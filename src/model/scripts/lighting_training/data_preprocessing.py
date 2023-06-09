import argparse
from openthaigpt_pretraining_model.data_wrapper import (
    TokenizedDataset,
)
from openthaigpt_pretraining_model.datasets import get_dataset
from openthaigpt_pretraining_model.datasets.constants import SPLIT_TRAIN, SPLIT_VAL
from re import findall
from transformers import (
    AutoTokenizer,
    LlamaTokenizer,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        type=str,
        default="train",
        help="train | val",
    )
    parser.add_argument(
        "--tokenizer",
        type=str,
        default="decapoda-research/llama-7b-hf",
        help="train | val",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=2048,
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default="./tokendata",
    )
    parser.add_argument(
        "--chunk_size",
        type=int,
        default=1024 * 1024,
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=25000,
    )
    parser.add_argument(
        "--num_proc",
        type=int,
        default=128,
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="oscar",
    )
    parser.add_argument(
        "--split",
        type=str,
        default=SPLIT_TRAIN,
        help=f"{SPLIT_TRAIN} | {SPLIT_VAL}",
    )
    args = parser.parse_args()
    print(args)
    dataset = get_dataset(dataset_name=args.dataset, split=args.split)
    if len(findall("llama", args.tokenizer)):
        tokenizer = LlamaTokenizer.from_pretrained(args.tokenizer)
        tokenizer.pad_token = "<pad>"
        tokenizer.add_special_tokens({"pad_token": "<pad>"})
    else:
        tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)

    dataset = TokenizedDataset(
        dataset=dataset,
        split=args.split,
        tokenizer=tokenizer,
        max_tokens=args.max_tokens,
        save_path=args.save_path,
        chunk_size=args.chunk_size,
        batch_size=args.batch_size,
        num_proc=args.num_proc,
    )
    dataset.tokenize_data()