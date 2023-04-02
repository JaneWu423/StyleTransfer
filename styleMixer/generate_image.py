import argparse
import os
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

# transform = transforms.Compose([
#     transforms.ToTensor()
# ])

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

    name = "styleMixer_bw1_style3.00_cont3.00_iden1.00_cx3.00_1"
    bandwidth = 1
    iter = 8
    mw = './styleMixer/checkpoint/'
    c = 6
    loc_weight = 3
    alpha = 1

    setting = name.split('_')
    if setting[2][:2]=='bw':
        bandwidth = setting[1][-1]
    mw += "%s/iter_%d0000.pth.tar" % (name, iter)


    #device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    device = torch.device("cpu")


    network = net.Net(vgg = 'styleMixer/checkpoint/vgg_normalised.pth')
    network.load_state_dict(torch.load(mw, map_location=torch.device('cpu')))
    network.eval()
    network.to(device)

    content_tf = test_transform()
    style_tf = test_transform()


    styles = style_tf(Image.open(style_file).convert('RGB'))
    #styles = [style.unsqueeze(0) for style in styles]
    styles = styles.to(device).unsqueeze(0)
    styles = styles.to(device).unsqueeze(0)
    #print("styles", styles[0].size())

    content = content_tf(Image.open(content_file).convert('RGB'))
    #print("content", content.size())
    content = content.to(device).unsqueeze(0)       

    # print("styles", styles[0].size())
    # print("content", content.size())
    
    with torch.no_grad():
        output = style_transfer(network=network, content=content, style=styles, device=device)
    
    # output = tensor2image(output.data)
    # output = Image.fromarray(output)
    grid = make_grid(output)
    ndarr = grid.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to("cpu", torch.uint8).numpy()
    im = Image.fromarray(ndarr)

    return im