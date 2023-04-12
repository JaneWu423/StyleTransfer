import torch
import os

device = torch.device("cpu")

batch_size = 4
lr = 0.001
T = 2
CONTENT_WEIGHT = 1
STYLE_WEIGHT = 1000000
REG_WEIGHT = 1e-5

continue_training = True


# ENCODER_WEIGHT_PATH = './stylebank/weights/encoder.pth'
# DECODER_WEIGHT_PATH = './stylebank/weights/decoder.pth'
# MODEL_WEIGHT_PATH = './stylebank/weights/model.pth'
NUM_STYLE = 3


CONTENT_IMG_DIR = '/content/drive/MyDrive/Stylebank/coco'
STYLE_IMG_DIR = '/content/drive/MyDrive/Stylebank/style_img'
MODEL_WEIGHT_DIR = './stylebank/weights'
BANK_WEIGHT_DIR = os.path.join(MODEL_WEIGHT_DIR, 'new_bank_2_23')
BANK_WEIGHT_PATH = os.path.join(BANK_WEIGHT_DIR, '{}.pth')
MODEL_WEIGHT_PATH = os.path.join(MODEL_WEIGHT_DIR, 'model.pth')
ENCODER_WEIGHT_PATH = os.path.join(MODEL_WEIGHT_DIR, 'encoder.pth')
DECODER_WEIGHT_PATH = os.path.join(MODEL_WEIGHT_DIR, 'decoder.pth')
GLOBAL_STEP_PATH = os.path.join(MODEL_WEIGHT_DIR, 'global_step.log')

NEW_BANK_WEIGHT_DIR = os.path.join(MODEL_WEIGHT_DIR, 'new_bank_2_23')


NEW_BANK_WEIGHT_PATH = os.path.join(NEW_BANK_WEIGHT_DIR, '{}.pth')



BANK_WEIGHT_DIR_A = os.path.join(MODEL_WEIGHT_DIR, 'new_bank_ae_20')
BANK_WEIGHT_PATH_A = os.path.join(BANK_WEIGHT_DIR_A, '{}.pth')

NEW_BANK_WEIGHT_DIR_A = os.path.join(MODEL_WEIGHT_DIR, 'new_bank_ae_20')
NEW_BANK_WEIGHT_PATH_A = os.path.join(NEW_BANK_WEIGHT_DIR_A, '{}.pth')


BANK_WEIGHT_DIR_R = os.path.join(MODEL_WEIGHT_DIR, 'new_bank_real_20')
BANK_WEIGHT_PATH_R = os.path.join(BANK_WEIGHT_DIR_R, '{}.pth')

NEW_BANK_WEIGHT_DIR_R = os.path.join(MODEL_WEIGHT_DIR, 'new_bank_real_20')
NEW_BANK_WEIGHT_PATH_R = os.path.join(NEW_BANK_WEIGHT_DIR_R, '{}.pth')


BANK_WEIGHT_DIR_U = os.path.join(MODEL_WEIGHT_DIR, 'new_bank_uki_20')
BANK_WEIGHT_PATH_U = os.path.join(BANK_WEIGHT_DIR_U, '{}.pth')

NEW_BANK_WEIGHT_DIR_U = os.path.join(MODEL_WEIGHT_DIR, 'new_bank_uki_20')
NEW_BANK_WEIGHT_PATH_U = os.path.join(NEW_BANK_WEIGHT_DIR_U, '{}.pth')


K = 1000
MAX_ITERATION = 300 * K
ADJUST_LR_ITER = 10 * K
LOG_ITER = 1 * K