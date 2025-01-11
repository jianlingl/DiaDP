
from typing import *
import random
import datetime

import os
import yaml
import wandb
import torch
from torch.utils.data import DataLoader, Subset
from transformers import AutoTokenizer

from trainer import InterTrainer
from model import DepParser, InterParser
from utils import arc_rel_loss, uas_las, seed_everything

from data_helper import SynDataset, DialogUttrInterDataset
from evaluation import eval_all_new

os.environ['CUDA_VISIBLE_DEVICES'] = '7'


def run():
    from config import DataClassUnpack, CFG
    # load_config
    with open('config/inter.yaml', 'r') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    CFG = DataClassUnpack.instantiate(CFG, config)
    CFG.debug = False

    wandb.init(project="Dialogue-Dep-Aug", entity="zzoay")
    if 'alpha' in wandb.config:
        del CFG.alpha
        print('Duplicate parameters deleted.')
    if 'aug_files' in wandb.config:
        del CFG.aug_files
        print('Duplicate parameters deleted.')
    wandb.config.update(CFG)
    CFG.aug_files = wandb.config.aug_files

    tokenizer = AutoTokenizer.from_pretrained(CFG.plm)
    special_tokens_dict = {'additional_special_tokens': ['[Q]', '[A]']}
    num_added_tokens = tokenizer.add_tokens(special_tokens_dict['additional_special_tokens'])
    print('token added', num_added_tokens, 'token')
    CFG.tokenizer = tokenizer

    traindataset = DialogUttrInterDataset(CFG, CFG.train_file, tokenizer)
    syndataset = SynDataset(CFG, tokenizer)

    syn_iter = DataLoader(syndataset, batch_size=CFG.syn_batch_size, shuffle=True, drop_last=True)

    one_epoch_steps = int(len(syndataset) / CFG.syn_batch_size)

    # alignment
    if not CFG.debug:
        n = int(one_epoch_steps / len(traindataset) * CFG.dialog_batch_size)
        rst_ids = list(range(len(traindataset)))
        tmp_ids = []
        for i in range(n):
            tmp_ids.extend(rst_ids)

        remain_num = one_epoch_steps - int(n * len(traindataset) / CFG.dialog_batch_size)
        random.shuffle(rst_ids)
        tmp_ids.extend(rst_ids[:remain_num])
        traindataset_extend = Subset(traindataset, tmp_ids)
        train_iter = DataLoader(traindataset_extend, batch_size=CFG.dialog_batch_size, shuffle=True)

    print("Train Size: " + str(len(traindataset_extend)))

    model = InterParser(CFG)
    wandb.watch(model)

    trainer = InterTrainer(model, one_epoch_steps=one_epoch_steps, loss_fn=arc_rel_loss, metrics_fn=uas_las, config=CFG)

    best_res, best_state_dict = trainer.train(model, train_iter, syn_iter)

    torch.save(best_state_dict, 'ckpt/inter_par.pt')

    # diagdataset_test = DialogUttrDataset(CFG, CFG.test_file, tokenizer, test=True)
    diagdataset_test = DialogUttrInterDataset(CFG, CFG.test_file, tokenizer, test=True)
    test_iter = DataLoader(diagdataset_test, batch_size=1, shuffle=True)

    # inter_dataset = InterDataset(CFG)
    # inter_iter = DataLoader(inter_dataset, batch_size=1)
    (inner_uas, inner_las), (inter_uas, inter_las) = eval_all_new(model, test_iter)
    wandb.log({"inner-EDU": {"uas": inner_uas, "las": inner_las}, 
               "inter-EDU": {"uas": inter_uas, "las": inter_las}})
    print((inner_uas, inner_las), (inter_uas, inter_las))
    

if __name__ == '__main__':
    seed_everything(42)

    debug = False
    use_wandb = True
    sweep = False

    # wandb
    if debug:
        os.environ['WANDB_MODE'] = 'disabled'  # offline / disabled

    if not use_wandb:
        os.environ['WANDB_MODE'] = 'disabled'  # offline / disabled
    
    time_now = datetime.datetime.now().isoformat()
    print(f'=-=-=-=-=-=-=-=-={time_now}=-=-=-=-=-=-=-=-=-=')

    run()

    print('=================End=================')
    print(datetime.datetime.now().isoformat())
    print('=====================================')
