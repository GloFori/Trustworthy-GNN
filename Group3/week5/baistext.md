| 数据集       | Epoch | 正边预测准确率$\pm$方差% | 负边预测准确率$\pm$方差% | Loss$\pm$方差%    | 多度边预测准确率$\pm$方差% | 单度边预测准确率$\pm$方差% | 测试集多度边 | 测试集单度边 | 总体多度边 | 总体单度边 |
| :----------- | :---- | :----------------------- | :----------------------- | ----------------- | -------------------------- | -------------------------- | ------------ | ------------ | ---------- | ---------- |
| WikiRfa      | 400   | 0.8059$\pm$0.011         | 0.7676$\pm$0.632         | 0.64745$\pm$0.546 | 0.8068$\pm$0.004           | 0.6293$\pm$0.017           | 33349        | 718          | 166839     | 3496       |
| WikiElec     | 500   | 0.8136$\pm$0.005         | 0.8262$\pm$0.007         | 0.5816$\pm$0.001  | 0.8209$\pm$0.001           | 0.6135$\pm$0.09            | 20279        | 458          | 101394     | 2295       |
| BitcoinOTC   | 400   | 0.9022$\pm$0.002         | 0.8062$\pm$0.02          | 0.4545$\pm$0.08   | 0.8936$\pm$0.001           | 0.8458$\pm$0.036           | 6968         | 149          | 34764      | 828        |
| Bitcoinalpha | 500   | 0.9048$\pm$0.001         | 0.7349$\pm$0.044         | 0.3142$\pm$0.001  | 0.8956$\pm$0.001           | 0.8066$\pm$0.07            | 4740         | 97           | 23793      | 393        |


| 数据集       | pos     | neg     | multi   | single  | loss    |
| :----------- | :------ | :------ | :------ | :------ | :------ |
| WikiRfa      | 0.00011 | 0.00632 | 0.00004 | 0.00017 | 0.00546 |
| WikiElec     | 0.00005 | 0.00007 | 0.00001 | 0.0009  | 0.00001 |
| BitcoinOTC   | 0.00002 | 0.0002  | 0.00001 | 0.00036 | 0.00002 |
| Bitcoinalpha | 0.00001 | 0.00044 | 0.00001 | 0.0007  | 0.00001 |

| wikiRfa:
| Epoch: 400, Loss: 0.7952,pos: 0.8164,neg: 0.6095, multi_acc: 0.8038,single_acc: 0.6142
| Epoch: 400, Loss: 0.6094,pos: 0.8168,neg: 0.8060, multi_acc: 0.8179,single_acc: 0.6466
| Epoch: 400, Loss: 0.6112,pos: 0.8059,neg: 0.7961, multi_acc: 0.8071,single_acc: 0.6425
| Epoch: 400, Loss: 0.6135,pos: 0.7883,neg: 0.8221, multi_acc: 0.7988,single_acc: 0.6246
| Epoch: 400, Loss: 0.6081,pos: 0.8019,neg: 0.8045, multi_acc: 0.8064,single_acc: 0.6185


| WikiElec
| Epoch: 500, Loss: 0.5826,pos: 0.8105,neg: 0.8315, multi_acc: 0.8204,single_acc: 0.5931
| Epoch: 500, Loss: 0.5785,pos: 0.8230,neg: 0.8154, multi_acc: 0.8249,single_acc: 0.6500
| Epoch: 500, Loss: 0.5830,pos: 0.8201,neg: 0.8214, multi_acc: 0.8242,single_acc: 0.6469
| Epoch: 500, Loss: 0.5792,pos: 0.8117,neg: 0.8241, multi_acc: 0.8198,single_acc: 0.5748
| Epoch: 500, Loss: 0.5849,pos: 0.8027,neg: 0.8389, multi_acc: 0.8153,single_acc: 0.6026


| BitcoinOTC
| Epoch: 400, Loss: 0.4557,pos: 0.8946,neg: 0.8146, multi_acc: 0.8871,single_acc: 0.8658
| Epoch: 400, Loss: 0.4611,pos: 0.9034,neg: 0.8048, multi_acc: 0.8950,single_acc: 0.8280
| Epoch: 400, Loss: 0.4478,pos: 0.9049,neg: 0.7823, multi_acc: 0.8932,single_acc: 0.8703
| Epoch: 400, Loss: 0.4517,pos: 0.9054,neg: 0.8244, multi_acc: 0.8986,single_acc: 0.8397
| Epoch: 400, Loss: 0.4560,pos: 0.9026,neg: 0.8048, multi_acc: 0.8942,single_acc: 0.8252


| Bitcoinalpha
| Epoch: 500, Loss: 0.3143,pos: 0.9013,neg: 0.7687, multi_acc: 0.8954,single_acc: 0.7732
| Epoch: 500, Loss: 0.3177,pos: 0.9060,neg: 0.7427, multi_acc: 0.8971,single_acc: 0.7973
| Epoch: 500, Loss: 0.3121,pos: 0.9053,neg: 0.7068, multi_acc: 0.8933,single_acc: 0.8507
| Epoch: 500, Loss: 0.3106,pos: 0.9029,neg: 0.7199, multi_acc: 0.8930,single_acc: 0.7927
| Epoch: 500, Loss: 0.3162,pos: 0.9086,neg: 0.7362, multi_acc: 0.8990,single_acc: 0.8193
