import time
import os

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.datasets as datasets
import numpy as np
import torchvision.transforms as transforms

import stylebank.args as args
from PIL import Image
from stylebank.networks import LossNetwork, StyleBankNet

NUM_STYLE = 3



model = StyleBankNet(NUM_STYLE).to(args.device)

model.encoder_net.load_state_dict(torch.load(args.ENCODER_WEIGHT_PATH,map_location= args.device))
model.decoder_net.load_state_dict(torch.load(args.DECODER_WEIGHT_PATH,map_location=args.device))
state_dict = torch.load(args.MODEL_WEIGHT_PATH,map_location=args.device)
# model.load_state_dict(torch.load(args.MODEL_WEIGHT_PATH,map_location=args.device))
for i in range(NUM_STYLE):
    model.style_bank[i].load_state_dict(torch.load(args.BANK_WEIGHT_PATH.format(i),map_location=args.device))

def transformImage(file, style):
    image = Image.open(file).convert("RGB")

    toTensor = transforms.ToTensor()
    tensor_image = toTensor(image).unsqueeze(0)
    output_image = model(tensor_image, [style])


    # output_image = model(tensor_image)
    output = output_image.squeeze(0)
    to_pil_image = transforms.ToPILImage()
    output = to_pil_image(output)
    # output.show()

    return output

# if __name__ == "__main__":
#     transformImage("../testHorse.jpg", 2)