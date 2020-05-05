from torchvision import transforms
from torchvision import datasets
from torch.utils.data import DataLoader
from torchvision import models
from torch import optim
import torch.nn as nn
import torch
import time
import matplotlib.pyplot as plt
from PIL import Image

image_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(size=256, scale=(0.8, 1.0)),
        transforms.RandomRotation(degrees=15),
        transforms.RandomHorizontalFlip(),
        transforms.CenterCrop(size=224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ]),
    'valid': transforms.Compose([
        transforms.Resize(size=256),
        transforms.CenterCrop(size=224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ]),
    'test': transforms.Compose([
        transforms.Resize(size=256),
        transforms.CenterCrop(size=224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
}


def predict(model, test_image_name):
     
    transform = image_transforms['test']
 
    test_image = Image.open(test_image_name)
    # test_image = test_image.resize((224, 224), Image.ANTIALIAS)
    plt.imshow(test_image)
     
    test_image_tensor = transform(test_image)
 
    if torch.cuda.is_available():
        test_image_tensor = test_image_tensor.view(1, 3, 224, 224).cuda()
    else:
        test_image_tensor = test_image_tensor.view(1, 3, 224, 224)
     
    with torch.no_grad():
        model.eval()
        # Model outputs log probabilities
        out = model(test_image_tensor)
        ps = torch.exp(out)
        topk, topclass = ps.topk(1, dim=1)
        return out.data.cpu().numpy().argmax()


def make_prediction(model_path, image_path):
    class_names = {
        0: 'cardboard',
        1: 'glass',
        2: 'metal',
        3: 'paper',
        4: 'plastic',
        5: 'trash'
    }
    model = models.resnet50(pretrained=True)
    fc_inputs = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(fc_inputs, 256),
        nn.ReLU(),
        nn.Dropout(0.4),
        nn.Linear(256, 10),
        nn.LogSoftmax(dim=1)
    )
    model.load_state_dict(torch.load(model_path,  map_location=torch.device('cpu')))
    model.eval()
    value = predict(model, image_path)
    return class_names[value]

if __name__ == '__main__':
    print(make_prediction('./trashnet.pt', './test/metal2.jpg'))








 

