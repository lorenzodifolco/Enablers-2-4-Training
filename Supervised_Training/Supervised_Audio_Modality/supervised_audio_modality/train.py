# Python code here
import os
import torch

from pytorch_lightning import Trainer, seed_everything
from conf import CUSTOM_SETTINGS,MAIN_FOLDER
from supervised_dataset import SupervisedDataModule
from callbacks.setup_callbacks import setup_callbacks
from utils.init_utils import (init_augmentations, init_datamodule,
                              init_loggers, init_random_split, init_transforms,
                              setup_ssl_model)
from utils.utils import copy_file, generate_experiment_id, load_yaml_to_dict

from encoders.cnn1d import CNN1D,CNN1D1L
from classification_model import classification_model
from classifiers.linear import LinearClassifier

def run_supervised_training():
    print(CUSTOM_SETTINGS)
    splith_paths = {'train':"outputs/train.csv",'val':"outputs/val.csv",'test':"outputs/test.csv"}

    train_transforms = {}
    test_transforms = {}

    if 'transforms' in CUSTOM_SETTINGS.keys():
        train_transforms,test_transforms = init_transforms(CUSTOM_SETTINGS['transforms'])

    # for now, don't use augmentations during supervised training
    #if 'augmentations' in CUSTOM_SETTINGS.keys():
    #    augmentations = init_augmentations(CUSTOM_SETTINGS['augmentations'])

    datamodule = SupervisedDataModule(
        path=MAIN_FOLDER,
        batch_size=CUSTOM_SETTINGS['sup_config']['batch_size'],
        split=splith_paths,
        train_transforms=train_transforms,
        test_transforms=test_transforms,
        n_views=2,
        num_workers=2,
        #augmentations=augmentations
    )
    #initialise encoder
    encoder = CNN1D(len_seq=CUSTOM_SETTINGS["pre_processing_config"]['max_length']*CUSTOM_SETTINGS["pre_processing_config"]['target_sr'],
                    #TODO: find way to integrate path to json config file and use path.os.join()
                    # or get the infor from the pretraining used
                    pretrained="Supervised_Training\Supervised_Audio_Modality\outputs\SSL_Training\\test_encoder.pt",
                    **CUSTOM_SETTINGS["encoder_config"]['kwargs']
                    )
    
    #add classification head to encoder
    classifier = LinearClassifier(encoder.out_size,CUSTOM_SETTINGS['dataset_config']['number_of_labels']) 
    model = classification_model(encoder=encoder,classifier=classifier,**CUSTOM_SETTINGS['sup_config']['kwargs'])

    print(model)
    #init callbacks  # initialize callbacks
    callbacks = setup_callbacks(
        early_stopping_metric="val_loss",
        no_ckpt=False,
        patience=15,
    )
    # initialize Pytorch-Lightning Training
    trainer = Trainer(
        #logger=loggers,
        #accelerator='cpu' if args.gpus == 0 else 'gpu',
        #devices=None if args.gpus == 0 else args.gpus,
        deterministic=True, 
        default_root_dir=os.path.join(MAIN_FOLDER,'outputs','Sup_Training'),
        callbacks=callbacks,
        max_epochs=CUSTOM_SETTINGS['sup_config']['epochs']
    )

    # pre-train and report test loss
    trainer.fit(model, datamodule)
    metrics = trainer.test(model, datamodule, ckpt_path='best')
    print(metrics)

    #save weights
    #torch.save(encoder.state_dict(), os.path.join(MAIN_FOLDER,'outputs','Sup_Training','test_model.pt'))

    pass

if __name__ == '__main__':
    run_supervised_training()