#!/usr/bin/env python
# coding: utf-8

from gatedGan.models import *
from gatedGan.data import *

# ##### Initialize Generator
gen = Generator(3, 3, 3, 64)
gen.load_state_dict(torch.load('./gatedGan/netG1000.pth', map_location='cpu'))

# ###### Define Image Transforms
transforms_ = [
    # transforms.Resize(int(300), transforms.InterpolationMode.BICUBIC),
    # transforms.RandomCrop(256),
    #         transforms.RandomVerticalFlip(p=0),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
]

transform = transforms.Compose(transforms_)



def tensor2image(tensor):
    image = 127.5 * (tensor[0].cpu().float().detach().numpy() + 1.0)
    return image.astype(np.uint8)


def generate_image(style, file, flip90=False):
    image = Image.open(file).convert("RGB")
    Abstract_Expressionism, Realism, Ukiyo_e, ident = style[0],style[1], style[2], style[3]
    content = transform(image)
    Tensor = torch.Tensor
    size = content.size()
    input_A = Tensor(1, 3, size[1], size[2])
    real_A = input_A.copy_(content)

    generated = gen({
        'content': real_A,
        'style_label': [[Abstract_Expressionism, Realism, Ukiyo_e, ident]]
    })
    im = tensor2image(generated.data)
    if flip90:
        im = im.transpose(2, 1, 0)
    else:
        im = im.transpose(1, 2, 0)
    im = Image.fromarray(im)

    return im

