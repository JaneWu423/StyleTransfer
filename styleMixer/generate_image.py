import argparse
import os
import time
import torch
import torch.nn as nn
from PIL import Image
from os.path import basename
from os.path import splitext
from torchvision import transforms
from torchvision.utils import save_image
from torchvision.utils import make_grid
import styleMixer.model
import styleMixer.net as net
from styleMixer.function import adaptive_instance_normalization
from styleMixer.function import coral
import numpy as np
import torchvision.transforms as transforms


def test_transform():
    transform_list = []
    transform_list.append(transforms.ToTensor())
    transform = transforms.Compose(transform_list)
    return transform



def style_transfer(network, content, style, device, alpha=0.5, num_cluster=10, loc_weight=0.0):
    return network.multi_transfer(content, style, device, alpha=alpha, num_cluster=num_cluster, loc_weight=loc_weight)

def tensor2image(tensor):
    image = 127.5 * (tensor[0].cpu().float().detach().numpy() + 1.0)
    return image.astype(np.uint8)

def generate_image_styleMixer(style_file, content_file):
    start = time.time()



    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


    network = net.Net(vgg = 'styleMixer/checkpoint/vgg_normalised.pth')
    network.load_state_dict(torch.load("styleMixer/checkpoint/iter_80000.pth.tar", map_location=torch.device('cpu')))
    network.eval()
    network.to(device)

    content_tf = test_transform()
    style_tf = test_transform()

    max_dimension = 800

    styles = style_tf(Image.open(style_file).convert('RGB'))
    width = styles.shape[1]
    height = styles.shape[2]
    if width > max_dimension or height > max_dimension:
        if width > height:
            new_width = max_dimension
            new_height = int(height * max_dimension / width)
        else:
            new_width = int(width * max_dimension / height)
            new_height = max_dimension

        toResize = transforms.Resize([new_width, new_height], transforms.InterpolationMode.BICUBIC)
        styles = toResize(styles)

    styles = styles.to(device).unsqueeze(0)
    styles = styles.to(device).unsqueeze(0)

    content = content_tf(Image.open(content_file).convert('RGB'))

    width = content.shape[1]
    height = content.shape[2]
    if width > max_dimension or height > max_dimension:
        if width > height:
            new_width = max_dimension
            new_height = int(height * max_dimension / width)
        else:
            new_width = int(width * max_dimension / height)
            new_height = max_dimension

        toResize = transforms.Resize([new_width, new_height], transforms.InterpolationMode.BICUBIC)
        content = toResize(content)

    content = content.to(device).unsqueeze(0)       
    
    with torch.no_grad():
        output = style_transfer(network=network, content=content, style=styles, device=device)
    
    grid = make_grid(output)
    ndarr = grid.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to("cpu", torch.uint8).numpy()
    im = Image.fromarray(ndarr)

    return im, time.time() - start