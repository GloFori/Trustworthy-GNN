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
