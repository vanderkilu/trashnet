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


train_directory = '/content/drive/My Drive/data/train'
valid_directory = '/content/drive/My Drive/data/valid'
test_directory = '/content/drive/My Drive/data/test'
filepath = '/content/drive/My Drive/data/trashnet.pt'
 
# # Batch size
# bs = 32
 
# # Number of classes
# num_classes = 6
 
# # Load Data from folders
# data = {
#     'train': datasets.ImageFolder(root=train_directory, transform=image_transforms['train']),
#     'valid': datasets.ImageFolder(root=valid_directory, transform=image_transforms['valid']),
#     # 'test': datasets.ImageFolder(root=test_directory, transform=image_transforms['test'])
# }

# train_data_size = len(data['train'])
# valid_data_size = len(data['valid'])
# # test_data_size = len(data['test'])

# train_data = DataLoader(data['train'], batch_size=bs, shuffle=True)
# valid_data = DataLoader(data['valid'], batch_size=bs, shuffle=True)
# test_data = DataLoader(data['test'], batch_size=bs, shuffle=True)


# model  = models.resnet50(pretrained=True)
# for param in model.parameters():
#     param.requires_grad = False
# fc_inputs = model.fc.in_features
# model.fc = nn.Sequential(
#     nn.Linear(fc_inputs, 256),
#     nn.ReLU(),
#     nn.Dropout(0.4),
#     nn.Linear(256, 10),
#     nn.LogSoftmax(dim=1)
# )
# model = model.to('cuda:0')
# loss_criterion = nn.NLLLoss()
# optimizer = optim.Adam(model.parameters())
# device = torch.device("cuda:0")

# epochs = 20


# for epoch in range(epochs):
#     epoch_start = time.time()
#     print("Epoch: {}/{}".format(epoch+1, epochs))
     
#     # Set to training mode
#     model.train()
     
#     # Loss and Accuracy within the epoch
#     train_loss = 0.0
#     train_acc = 0.0
     
#     valid_loss = 0.0
#     valid_acc = 0.0
 
#     for i, (inputs, labels) in enumerate(train_data):
 
#         inputs = inputs.to(device)
#         labels = labels.to(device)
         
#         # Clean existing gradients
#         optimizer.zero_grad()
         
#         # Forward pass - compute outputs on input data using the model
#         outputs = model(inputs)
         
#         # Compute loss
#         loss = loss_criterion(outputs, labels)
         
#         # Backpropagate the gradients
#         loss.backward()
         
#         # Update the parameters
#         optimizer.step()
         
#         # Compute the total loss for the batch and add it to train_loss
#         train_loss += loss.item() * inputs.size(0)
         
#         # Compute the accuracy
#         ret, predictions = torch.max(outputs.data, 1)
#         correct_counts = predictions.eq(labels.data.view_as(predictions))
         
#         # Convert correct_counts to float and then compute the mean
#         acc = torch.mean(correct_counts.type(torch.FloatTensor))
         
#         # Compute total accuracy in the whole batch and add to train_acc
#         train_acc += acc.item() * inputs.size(0)
         
#         print("Batch number: {:03d}, Training: Loss: {:.4f}, Accuracy: {:.4f}".format(i, loss.item(), acc.item()))

#     with torch.no_grad():

#       # Set to evaluation mode
#       model.eval()
  
#       # Validation loop
#       for j, (inputs, labels) in enumerate(valid_data):
#           inputs = inputs.to(device)
#           labels = labels.to(device)
  
#           # Forward pass - compute outputs on input data using the model
#           outputs = model(inputs)
  
#           # Compute loss
#           loss = loss_criterion(outputs, labels)
  
#           # Compute the total loss for the batch and add it to valid_loss
#           valid_loss += loss.item() * inputs.size(0)
  
#           # Calculate validation accuracy
#           ret, predictions = torch.max(outputs.data, 1)
#           correct_counts = predictions.eq(labels.data.view_as(predictions))
  
#           # Convert correct_counts to float and then compute the mean
#           acc = torch.mean(correct_counts.type(torch.FloatTensor))
  
#           # Compute total accuracy in the whole batch and add to valid_acc
#           valid_acc += acc.item() * inputs.size(0)
  
#           print("Validation Batch number: {:03d}, Validation: Loss: {:.4f}, Accuracy: {:.4f}".format(j, loss.item(), acc.item()))

# torch.save(model.state_dict(), filepath)

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
        print("Output class :  ", out.data.cpu().numpy().argmax())

model = models.resnet50(pretrained=True)
fc_inputs = model.fc.in_features
model.fc = nn.Sequential(
    nn.Linear(fc_inputs, 256),
    nn.ReLU(),
    nn.Dropout(0.4),
    nn.Linear(256, 10),
    nn.LogSoftmax(dim=1)
)
model.load_state_dict(torch.load(filepath))
model.eval()
model = model.to('cuda:0')

predict(model, "/content/drive/My Drive/data/test/cardboard220.jpg")







 

