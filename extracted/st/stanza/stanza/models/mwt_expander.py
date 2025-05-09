"""
Entry point for training and evaluating a multi-word token (MWT) expander.

This MWT expander combines a neural sequence-to-sequence architecture with a dictionary
to decode the token into multiple words.
For details please refer to paper: https://nlp.stanford.edu/pubs/qi2018universal.pdf

In the case of a dataset where all of the MWT exactly split into the words
composing the MWT, a classifier over the characters is used instead of the seq2seq
"""

import sys
import os
import shutil
import time
from datetime import datetime
import argparse
import logging
import math
import numpy as np
import random
import torch
from torch import nn, optim
import copy

from stanza.models.mwt.data import DataLoader, BinaryDataLoader
from stanza.models.mwt.utils import mwts_composed_of_words
from stanza.models.mwt.vocab import Vocab
from stanza.models.mwt.trainer import Trainer
from stanza.models.mwt import scorer
from stanza.models.common import utils
import stanza.models.common.seq2seq_constant as constant
from stanza.models.common.doc import Document
from stanza.utils.conll import CoNLL
from stanza.models import _training_logging

logger = logging.getLogger('stanza')

def build_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data/mwt', help='Root dir for saving models.')
    parser.add_argument('--train_file', type=str, default=None, help='Input file for data loader.')
    parser.add_argument('--eval_file', type=str, default=None, help='Input file for data loader.')
    parser.add_argument('--output_file', type=str, default=None, help='Output CoNLL-U file.')
    parser.add_argument('--gold_file', type=str, default=None, help='Output CoNLL-U file.')

    parser.add_argument('--mode', default='train', choices=['train', 'predict'])
    parser.add_argument('--lang', type=str, help='Language')
    parser.add_argument('--shorthand', type=str, help="Treebank shorthand")

    parser.add_argument('--no_dict', dest='ensemble_dict', action='store_false', help='Do not ensemble dictionary with seq2seq. By default ensemble a dict.')
    parser.add_argument('--ensemble_early_stop', action='store_true', help='Early stopping based on ensemble performance.')
    parser.add_argument('--dict_only', action='store_true', help='Only train a dictionary-based MWT expander.')

    parser.add_argument('--hidden_dim', type=int, default=100)
    parser.add_argument('--emb_dim', type=int, default=50)
    parser.add_argument('--num_layers', type=int, default=None, help='Number of layers in model encoder.  Defaults to 1 for seq2seq, 2 for classifier')
    parser.add_argument('--emb_dropout', type=float, default=0.5)
    parser.add_argument('--dropout', type=float, default=0.5)
    parser.add_argument('--max_dec_len', type=int, default=50)
    parser.add_argument('--beam_size', type=int, default=1)
    parser.add_argument('--attn_type', default='soft', choices=['soft', 'mlp', 'linear', 'deep'], help='Attention type')
    parser.add_argument('--no_copy', dest='copy', action='store_false', help='Do not use copy mechanism in MWT expansion. By default copy mechanism is used to improve generalization.')

    parser.add_argument('--augment_apos', default=0.01, type=float, help='At training time, how much to augment |\'| to |"| |’| |ʼ|')
    parser.add_argument('--force_exact_pieces', default=None, action='store_true', help='If possible, make the text of the pieces of the MWT add up to the token itself.  (By default, this is determined from the dataset.)')
    parser.add_argument('--no_force_exact_pieces', dest='force_exact_pieces', action='store_false', help="Don't make the text of the pieces of the MWT add up to the token itself.  (By default, this is determined from the dataset.)")

    parser.add_argument('--sample_train', type=float, default=1.0, help='Subsample training data.')
    parser.add_argument('--optim', type=str, default='adam', help='sgd, adagrad, adam or adamax.')
    parser.add_argument('--lr', type=float, default=1e-3, help='Learning rate')
    parser.add_argument('--lr_decay', type=float, default=0.9)
    parser.add_argument('--decay_epoch', type=int, default=30, help="Decay the lr starting from this epoch.")
    parser.add_argument('--num_epoch', type=int, default=30)
    parser.add_argument('--batch_size', type=int, default=50)
    parser.add_argument('--max_grad_norm', type=float, default=5.0, help='Gradient clipping.')
    parser.add_argument('--log_step', type=int, default=20, help='Print log every k steps.')
    parser.add_argument('--save_dir', type=str, default='saved_models/mwt', help='Root dir for saving models.')
    parser.add_argument('--save_name', type=str, default=None, help="File name to save the model")
    parser.add_argument('--save_each_name', type=str, default=None, help="Save each model in sequence to this pattern.  Mostly for testing")

    parser.add_argument('--seed', type=int, default=1234)
    utils.add_device_args(parser)

    parser.add_argument('--wandb', action='store_true', help='Start a wandb session and write the results of training.  Only applies to training.  Use --wandb_name instead to specify a name')
    parser.add_argument('--wandb_name', default=None, help='Name of a wandb session to start when training.  Will default to the dataset short name')
    return parser

def parse_args(args=None):
    parser = build_argparse()
    args = parser.parse_args(args=args)

    if args.wandb_name:
        args.wandb = True

    return args

def main(args=None):
    args = parse_args(args=args)

    utils.set_random_seed(args.seed)

    args = vars(args)
    logger.info("Running MWT expander in {} mode".format(args['mode']))

    if args['mode'] == 'train':
        train(args)
    else:
        evaluate(args)

def train(args):
    # load data
    logger.debug('max_dec_len: %d' % args['max_dec_len'])
    logger.debug("Loading data with batch size {}...".format(args['batch_size']))
    train_doc = CoNLL.conll2doc(input_file=args['train_file'])
    train_batch = DataLoader(train_doc, args['batch_size'], args, evaluation=False)
    vocab = train_batch.vocab
    args['vocab_size'] = vocab.size
    dev_doc = CoNLL.conll2doc(input_file=args['eval_file'])
    dev_batch = DataLoader(dev_doc, args['batch_size'], args, vocab=vocab, evaluation=True)

    utils.ensure_dir(args['save_dir'])
    save_name = args['save_name'] if args['save_name'] else '{}_mwt_expander.pt'.format(args['shorthand'])
    model_file = os.path.join(args['save_dir'], save_name)

    save_each_name = None
    if args['save_each_name']:
        save_each_name = os.path.join(args['save_dir'], args['save_each_name'])
        save_each_name = utils.build_save_each_filename(save_each_name)

    # pred and gold path
    system_pred_file = args['output_file']
    gold_file = args['gold_file']

    # skip training if the language does not have training or dev data
    if len(train_batch) == 0:
        logger.warning("Skip training because no data available...")
        return
    dev_mwt = dev_doc.get_mwt_expansions(False)
    if len(dev_batch) == 0 and args.get('dict_only', False):
        logger.warning("Training data available, but dev data has no MWTs.  Only training a dict based MWT")
        args['dict_only'] = True

    if args['force_exact_pieces'] and not mwts_composed_of_words(train_doc):
        raise ValueError("Cannot train model with --force_exact_pieces, as the MWT in this dataset are not entirely composed of their subwords")

    if args['force_exact_pieces'] is None and mwts_composed_of_words(train_doc):
        # the force_exact_pieces mechanism trains a separate version of the MWT expander in the Trainer
        # (the training loop here does not need to change)
        # in this model, a classifier distinguishes whether or not a location is a split
        # and the text is copied exactly from the input rather than created via seq2seq
        # this behavior can be turned off at training time with --no_force_exact_pieces
        logger.info("Train MWTs entirely composed of their subwords.  Training the MWT to match that paradigm as closely as possible")
        args['force_exact_pieces'] = True

    if args['force_exact_pieces']:
        logger.info("Reconverting to BinaryDataLoader")
        train_batch = BinaryDataLoader(train_doc, args['batch_size'], args, evaluation=False)
        vocab = train_batch.vocab
        args['vocab_size'] = vocab.size
        dev_batch = BinaryDataLoader(dev_doc, args['batch_size'], args, vocab=vocab, evaluation=True)

    if args['num_layers'] is None:
        if args['force_exact_pieces']:
            args['num_layers'] = 2
        else:
            args['num_layers'] = 1

    # train a dictionary-based MWT expander
    trainer = Trainer(args=args, vocab=vocab, device=args['device'])
    logger.info("Training dictionary-based MWT expander...")
    trainer.train_dict(train_batch.doc.get_mwt_expansions(evaluation=False))
    logger.info("Evaluating on dev set...")
    dev_preds = trainer.predict_dict(dev_batch.doc.get_mwt_expansions(evaluation=True))
    doc = copy.deepcopy(dev_batch.doc)
    doc.set_mwt_expansions(dev_preds, fake_dependencies=True)
    CoNLL.write_doc2conll(doc, system_pred_file)
    _, _, dev_f = scorer.score(system_pred_file, gold_file)
    logger.info("Dev F1 = {:.2f}".format(dev_f * 100))

    if args.get('dict_only', False):
        # save dictionaries
        trainer.save(model_file)
    else:
        # train a seq2seq model
        logger.info("Training seq2seq-based MWT expander...")
        global_step = 0
        steps_per_epoch = math.ceil(len(train_batch) / args['batch_size'])
        max_steps = steps_per_epoch * args['num_epoch']
        dev_score_history = []
        best_dev_preds = []
        current_lr = args['lr']
        global_start_time = time.time()
        format_str = '{}: step {}/{} (epoch {}/{}), loss = {:.6f} ({:.3f} sec/batch), lr: {:.6f}'

        if args['wandb']:
            import wandb
            wandb_name = args['wandb_name'] if args['wandb_name'] else "%s_mwt" % args['shorthand']
            wandb.init(name=wandb_name, config=args)
            wandb.run.define_metric('train_loss', summary='min')
            wandb.run.define_metric('dev_score', summary='max')

        # start training
        for epoch in range(1, args['num_epoch']+1):
            train_loss = 0
            for i, batch in enumerate(train_batch.to_loader()):
                start_time = time.time()
                global_step += 1
                loss = trainer.update(batch, eval=False) # update step
                train_loss += loss
                if global_step % args['log_step'] == 0:
                    duration = time.time() - start_time
                    logger.info(format_str.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), global_step,\
                                                  max_steps, epoch, args['num_epoch'], loss, duration, current_lr))

            if save_each_name:
                trainer.save(save_each_name % epoch)
                logger.info("Saved epoch %d model to %s" % (epoch, save_each_name % epoch))

            # eval on dev
            logger.info("Evaluating on dev set...")
            dev_preds = []
            for i, batch in enumerate(dev_batch.to_loader()):
                preds = trainer.predict(batch)
                dev_preds += preds
            if args.get('ensemble_dict', False) and args.get('ensemble_early_stop', False):
                logger.info("[Ensembling dict with seq2seq model...]")
                dev_preds = trainer.ensemble(dev_batch.doc.get_mwt_expansions(evaluation=True), dev_preds)
            doc = copy.deepcopy(dev_batch.doc)
            doc.set_mwt_expansions(dev_preds, fake_dependencies=True)
            CoNLL.write_doc2conll(doc, system_pred_file)
            _, _, dev_score = scorer.score(system_pred_file, gold_file)
            train_loss = train_loss / train_batch.num_examples * args['batch_size'] # avg loss per batch
            logger.info("epoch {}: train_loss = {:.6f}, dev_score = {:.4f}".format(epoch, train_loss, dev_score))

            if args['wandb']:
                wandb.log({'train_loss': train_loss, 'dev_score': dev_score})

            # save best model
            if epoch == 1 or dev_score > max(dev_score_history):
                trainer.save(model_file)
                logger.info("new best model saved.")
                best_dev_preds = dev_preds

            # lr schedule
            if epoch > args['decay_epoch'] and dev_score <= dev_score_history[-1]:
                current_lr *= args['lr_decay']
                trainer.change_lr(current_lr)

            dev_score_history += [dev_score]

        logger.info("Training ended with {} epochs.".format(epoch))

        if args['wandb']:
            wandb.finish()

        best_f, best_epoch = max(dev_score_history)*100, np.argmax(dev_score_history)+1
        logger.info("Best dev F1 = {:.2f}, at epoch = {}".format(best_f, best_epoch))

        # try ensembling with dict if necessary
        if args.get('ensemble_dict', False):
            logger.info("[Ensembling dict with seq2seq model...]")
            dev_preds = trainer.ensemble(dev_batch.doc.get_mwt_expansions(evaluation=True), best_dev_preds)
            doc = copy.deepcopy(dev_batch.doc)
            doc.set_mwt_expansions(dev_preds, fake_dependencies=True)
            CoNLL.write_doc2conll(doc, system_pred_file)
            _, _, dev_score = scorer.score(system_pred_file, gold_file)
            logger.info("Ensemble dev F1 = {:.2f}".format(dev_score*100))
            best_f = max(best_f, dev_score)

def evaluate(args):
    # file paths
    system_pred_file = args['output_file']
    gold_file = args['gold_file']
    model_file = args['save_name'] if args['save_name'] else '{}_mwt_expander.pt'.format(args['shorthand'])
    if args['save_dir'] and not model_file.startswith(args['save_dir']) and not os.path.exists(model_file):
        model_file = os.path.join(args['save_dir'], model_file)

    # load model
    trainer = Trainer(model_file=model_file, device=args['device'])
    loaded_args, vocab = trainer.args, trainer.vocab

    for k in args:
        if k.endswith('_dir') or k.endswith('_file') or k in ['shorthand']:
            loaded_args[k] = args[k]
    logger.debug('max_dec_len: %d' % loaded_args['max_dec_len'])

    # load data
    logger.debug("Loading data with batch size {}...".format(args['batch_size']))
    doc = CoNLL.conll2doc(input_file=args['eval_file'])
    batch = DataLoader(doc, args['batch_size'], loaded_args, vocab=vocab, evaluation=True)

    if len(batch) > 0:
        dict_preds = trainer.predict_dict(batch.doc.get_mwt_expansions(evaluation=True))
        # decide trainer type and run eval
        if loaded_args['dict_only']:
            preds = dict_preds
        else:
            logger.info("Running the seq2seq model...")
            preds = []
            for i, b in enumerate(batch.to_loader()):
                preds += trainer.predict(b)

            if loaded_args.get('ensemble_dict', False):
                preds = trainer.ensemble(batch.doc.get_mwt_expansions(evaluation=True), preds)
    else:
        # skip eval if dev data does not exist
        preds = []

    # write to file and score
    doc = copy.deepcopy(batch.doc)
    doc.set_mwt_expansions(preds, fake_dependencies=True)
    CoNLL.write_doc2conll(doc, system_pred_file)

    if gold_file is not None:
        _, _, score = scorer.score(system_pred_file, gold_file)

        logger.info("MWT expansion score: {} {:.2f}".format(args['shorthand'], score*100))


if __name__ == '__main__':
    main()
