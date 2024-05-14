def compute_multi_degree_edge_accuracy(
        self,
        degrees: torch.Tensor,
        pos_edge_index: torch.Tensor,
        neg_edge_index: torch.Tensor,
        z: Tensor,
) -> tuple[float | int | Any, float | int | Any]:
    pos_p, neg_p = self.test_pos_eng(z, pos_edge_index, neg_edge_index)
    multi_correct_predictions = 0
    single_correct_predictions = 0
    m = 0
    s = 0
    k = 1
    for i in range(pos_edge_index.size(1)):
        src, dst = pos_edge_index[:, i]
        if pos_p[i] == 0:
            if degrees[src] <= k or degrees[dst] <= k:
                single_correct_predictions = single_correct_predictions + 1
                s = s + 1
            else:
                multi_correct_predictions = multi_correct_predictions + 1
                m = m + 1

        else:
            if degrees[src] <= k or degrees[dst] <= k:
                s = s + 1
            else:
                m = m + 1
    for i in range(neg_edge_index.size(1)):
        src, dst = neg_edge_index[:, i]
        if neg_p[i] == 1:
            if degrees[src] <= k or degrees[dst] <= k:
                single_correct_predictions = single_correct_predictions + 1
                s = s + 1
            else:
                multi_correct_predictions = multi_correct_predictions + 1
                m = m + 1

        else:
            if degrees[src] <= k or degrees[dst] <= k:
                s = s + 1
            else:
                m = m + 1

    # 计算预测正确概率
    if m != 0:
        multi_acc = multi_correct_predictions / m
    else:
        multi_acc = 0
    if s != 0:
        single_acc = single_correct_predictions / s
    else:
        single_acc = 0
    # print(m)
    # print(s)
    return multi_acc, single_acc


def test_pos_eng(
        self,
        z: Tensor,
        pos_edge_index: Tensor,
        neg_edge_index: Tensor,
) -> Tuple[Tensor, Tensor]:
    with torch.no_grad():
        pos_p = self.discriminate(z, pos_edge_index)[:, :2].max(dim=1)[1]
        neg_p = self.discriminate(z, neg_edge_index)[:, :2].max(dim=1)[1]
    return pos_p, neg_p


import torch
from torch_geometric.data import Data
from torch_geometric.nn import SignedGCN

# 读取txt数据并转换成图数据对象
def read_txt_data(file_path):
    edge_index = []
    edge_attr = []

    with open(file_path, 'r') as f:
        for line in f:
            src, dst, attr = map(int, line.strip().split())  # 假设每行是两个节点的编号和边属性
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
data = read_txt_data('./data/WikiElec.txt')
# Generate dataset.
pos_edge_indices, neg_edge_indices = [], []
pos_edge_indices.append(data.edge_index[:, data.edge_attr > 0])
neg_edge_indices.append(data.edge_index[:, data.edge_attr < 0])



# 计算每个节点的度数
combined_edge_index = torch.cat([pos_edge_index, neg_edge_index], dim=1)
N = combined_edge_index.max().item() + 1
degrees = torch.zeros(N, dtype=torch.long)
for i in range(combined_edge_index.size(1)):
    src, dst = combined_edge_index[:, i]
    degrees[src] += 1
    degrees[dst] += 1

# 统计多度边
multi=0
single=0
for i in range(combined_edge_index.size(1)):
    src, dst = combined_edge_index[:, i]
    if degrees[src] <= 1 or degrees[dst] <= 1:
        single=single + 1
    else:
        multi = multi + 1
#print(multi)
#print(single)

#统计
import numpy as np
import matplotlib.pyplot as plt

'''
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

for epoch in range(401):
    loss = train()
    pos_p, neg_p = test1()
    pos_p_mean = 1 - pos_p.float().mean().item()
    neg_p_mean = neg_p.float().mean().item()
    multi_acc, single_acc = test2()
    print(f'Epoch: {epoch:03d}, Loss: {loss:.4f},pos: {pos_p_mean :.4f},neg: {neg_p_mean :.4f}, multi_acc: {multi_acc:.4f},single_acc: { single_acc:.4f}')
