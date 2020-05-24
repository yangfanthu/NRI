import torch
import torch.nn as nn
# import torchvision
import numpy as np
import pdb
class BallDataset(torch.utils.data.Dataset):
	def __init__(self):
		data_path = './data/balls/balls.npy'
		self.data = np.load(data_path)
		self.data = torch.from_numpy(self.data).float()
	def __getitem__(self, index):
		data = self.data[index,:,:,:]
		return data
	def __len__(self):
		return len(self.data)


if __name__ == "__main__":
	dataset = BallDataset()
	train_ratio = 0.8
	train_num = int(len(dataset.data) * train_ratio)
	test_num = len(dataset.data) - train_num
	data_num = [train_num, test_num]
	train_set, test_set = torch.utils.data.random_split(dataset, data_num)
	train_loader = torch.utils.data.DataLoader(dataset = train_set, batch_size = 4, shuffle = False)
	test_loader = torch.utils.data.DataLoader(dataset = test_set, batch_size = 4, shuffle = False)
	data_iter = iter(train_loader)
	data, agent_num, rel_rec, rel_send, agent_type = data_iter.next()
	print(data)
	print(agent_num)
