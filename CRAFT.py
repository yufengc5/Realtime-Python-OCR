import sys
import os

sys.path.append(os.path.abspath('CRAFT-pytorch'))

import cv2
import numpy as np
from craft import CRAFT  
from craft_test import copyStateDict, test_net
import torch
import torch.backends.cudnn as cudnn


# Initialize CRAFT model and load weights
def load_craft_model(model_path, cuda=False, refine=False):
    refiner_model = "CRAFT-pytorch/weights/craft_refiner_CTW1500.pth"
    net = CRAFT()
    if cuda:
        net.load_state_dict(copyStateDict(torch.load(model_path)))
    else:
        net.load_state_dict(copyStateDict(torch.load(model_path, map_location='cpu')))
    if cuda:
        net = net.cuda()
        net = torch.nn.DataParallel(net)
        cudnn.benchmark = False
    net.eval()

    refine_net = None
    if refine:
        from refinenet import RefineNet
        refine_net = RefineNet()
        print('Loading weights of refiner from checkpoint (' + refiner_model + ')')
        if cuda:
            refine_net.load_state_dict(copyStateDict(torch.load(refiner_model)))
            refine_net = refine_net.cuda()
            refine_net = torch.nn.DataParallel(refine_net)
        else:
            refine_net.load_state_dict(copyStateDict(torch.load(refiner_model, map_location='cpu')))
        refine_net.eval()
    return net

# Run CRAFT on an image
def detect_text_regions(image, model):
    text_threshold = 0.7
    link_threshold = 0.4
    low_text = 0.4
    cuda = torch.cuda.is_available()
    poly = False
    refine_net = None  
    # Assuming the image is already in BGR format (OpenCV)
    bboxes, polys, score_text = test_net(model, image, text_threshold, link_threshold, low_text, cuda, poly, refine_net=None)
    return bboxes

def run_CRAFT(img_path):
    # Load image
    img = cv2.imread(img_path)

    # Load CRAFT model
    net = load_craft_model("CRAFT-pytorch/weights/craft_mlt_25k.pth", cuda=torch.cuda.is_available())
    # Detect text regions
    boxes = detect_text_regions(img, net)
    return boxes
    #print("Detected boxes:", boxes)
