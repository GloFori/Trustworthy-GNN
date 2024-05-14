'''
import os.path as osp
import torch
from torch_geometric.datasets import BitcoinOTC
from torch_geometric.nn import SignedGCN

name = 'BitcoinOTC-1'
path = osp.join(osp.dirname(osp.realpath(__file__)), '..', 'data', name)
dataset = BitcoinOTC(path, edge_window_size=1)

# Generate dataset.
pos_edge_indices, neg_edge_indices = [], []
for data in dataset:
    pos_edge_indices.append(data.edge_index[:, data.edge_attr > 0])
    neg_edge_indices.append(data.edge_index[:, data.edge_attr < 0])
'''

import torch
from torch_geometric.data import Data
from torch_geometric.nn import SignedGCN

# 读取txt数据并转换成图数据对象
def read_txt_data(file_path):
    edge_index = []
    edge_attr = []

    with open(file_path, 'r') as f:
        for line in f:
            src, dst, attr,no= map(int, line.strip().split(','))  # 假设每行是两个节点的编号和边属性
            edge_index.append([src, dst])
            edge_attr.append(attr)

    # 将边列表和边属性列表转换为张量表示
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_attr, dtype=torch.float)  # 假设边属性是浮点数

    # 计算图的节点数
    num_nodes = edge_index.max().item() + 1

    # 创建图数据对象
    data = Data(edge_index=edge_index, edge_attr=edge_attr, num_nodes=num_nodes)

    return data

# 读取txt数据并转换成图数据对象
data = read_txt_data('./data/soc-sign-bitcoinalpha.csv')
# Generate dataset.
pos_edge_indices, neg_edge_indices = [], []
pos_edge_indices.append(data.edge_index[:, data.edge_attr > 0])
neg_edge_indices.append(data.edge_index[:, data.edge_attr < 0])

'''
import torch
from torch_geometric.data import Data
from torch_geometric.nn import SignedGCN

# 读取txt数据并转换成图数据对象
def read_txt_data(file_path):
    edge_index = []
    edge_attr = []

    with open(file_path, 'r') as f:
        for line in f:
            src, dst, attr= map(int, line.strip().split())  # 假设每行是两个节点的编号和边属性
            edge_index.append([src, dst])
            edge_attr.append(attr)

    # 将边列表和边属性列表转换为张量表示
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_attr, dtype=torch.float)  # 假设边属性是浮点数

    # 计算图的节点数
    num_nodes = edge_index.max().item() + 1

    # 创建图数据对象
    data = Data(edge_index=edge_index, edge_attr=edge_attr, num_nodes=num_nodes)

    return data

# 读取txt数据并转换成图数据对象
data = read_txt_data('./data/soc-sign-bitcoinalpha.csv')
# Generate dataset.
pos_edge_indices, neg_edge_indices = [], []
pos_edge_indices.append(data.edge_index[:, data.edge_attr > 0])
neg_edge_indices.append(data.edge_index[:, data.edge_attr < 0])
'''

if torch.cuda.is_available():
    device = torch.device('cuda')
elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
    device = torch.device('mps')
else:
    device = torch.device('cpu')

pos_edge_index = torch.cat(pos_edge_indices, dim=1).to(device)
neg_edge_index = torch.cat(neg_edge_indices, dim=1).to(device)

# 计算每个节点的度数
combined_edge_index = torch.cat([pos_edge_index, neg_edge_index], dim=1)
N = combined_edge_index.max().item() + 1
degrees = torch.zeros(N, dtype=torch.long)
for i in range(combined_edge_index.size(1)):
    src, dst = combined_edge_index[:, i]
    degrees[src] += 1
    degrees[dst] += 1
'''
# 统计多度边
multi=0
single=0
for i in range(combined_edge_index.size(1)):
    src, dst = combined_edge_index[:, i]
    if degrees[src] <= 1 or degrees[dst] <= 1:
        single=single + 1
    else:
        multi = multi + 1
print(multi)
print(single)

#统计
import numpy as np
import matplotlib.pyplot as plt


# 统计度的分布
degree_counts = np.bincount(degrees)

# 绘制度的分布统计图
plt.bar(range(len(degree_counts)), degree_counts, color='skyblue')
plt.xlim(0, 200)
plt.xlabel('Degree')
plt.ylabel('Count')
plt.title('Degree Distribution')
plt.show()

'''
# Build and train model.
model = SignedGCN(64, 64, num_layers=2, lamb=5).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

train_pos_edge_index, test_pos_edge_index = model.split_edges(pos_edge_index)
train_neg_edge_index, test_neg_edge_index = model.split_edges(neg_edge_index)
x = model.create_spectral_features(train_pos_edge_index, train_neg_edge_index)

def train():
    model.train()
    optimizer.zero_grad()
    z = model(x, train_pos_edge_index, train_neg_edge_index)
    loss = model.loss(z, train_pos_edge_index, train_neg_edge_index)
    loss.backward()
    optimizer.step()
    return loss.item()

def test1():
    model.eval()
    with torch.no_grad():
        z = model(x, train_pos_edge_index, train_neg_edge_index)
    return model.test_pos_eng(z, test_pos_edge_index, test_neg_edge_index)
def test2():
    model.eval()
    with torch.no_grad():
        z = model(x, train_pos_edge_index, train_neg_edge_index)
    return model.compute_multi_degree_edge_accuracy(degrees, test_pos_edge_index, test_neg_edge_index, z)

for epoch in range(501):
    loss = train()
    pos_p, neg_p = test1()
    pos_p_mean = 1 - pos_p.float().mean().item()
    neg_p_mean = neg_p.float().mean().item()
    multi_acc, single_acc = test2()
    print(f'Epoch: {epoch:03d}, Loss: {loss:.4f},pos: {pos_p_mean :.4f},neg: {neg_p_mean :.4f}, multi_acc: {multi_acc:.4f},single_acc: { single_acc:.4f}')
