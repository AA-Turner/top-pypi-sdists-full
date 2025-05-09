# Copyright (c) 2025, NVIDIA CORPORATION.
# SPDX-License-Identifier: BSD-3-Clause

import re
from typing import List, Optional

import click
import torch

from megatron.energon.epathlib import EPath
from megatron.energon.savable_loader import SavableDataLoaderState


def natural_sort_key(s):
    """
    Function to use for natural sorting of filenames.

    This splits the input string by numbers and non-numbers and ensures
    that numbers are compared as integers, not as strings.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)]


def detect_and_replicate_pattern(file_list):
    """
    Given a list of file paths, detect the single numeric pattern and return
    a function that, when called with integer n (starting from 0), generates
    the n-th filename following that pattern.

    Raises an Exception if no pattern or multiple patterns are found.
    """
    if not file_list:
        raise ValueError("Cannot detect a pattern from an empty list.")

    # -- 1) Sort the list using a natural key so that numbers compare numerically
    sorted_files = sorted(file_list, key=natural_sort_key)

    # -- 2) Tokenize each filename into [text, number, text, number, ...].
    #        We'll look for the pattern of tokens across all files.
    def tokenize_filename(fname):
        # Use the same split so that digit tokens are separated
        # from non-digit tokens.
        tokens = re.split(r"(\d+)", fname)
        # tokens is like ["f", "001", ".txt"] for "f001.txt"
        return tokens

    tokenized = [tokenize_filename(f) for f in sorted_files]

    # Check that all tokenized filenames have the same number of chunks:
    token_len = len(tokenized[0])
    for t in tokenized:
        if len(t) != token_len:
            raise Exception("Filenames do not share a consistent token structure.")

    # -- 3) Identify exactly one numeric token position that changes across all files.
    #        All other positions must be identical across the entire list.
    num_positions = []  # positions in the token list that differ
    for pos in range(token_len):
        # Check if this chunk is the same for all files or not:
        # We compare "raw text" for non-digit chunks, and "integer value" for digit chunks.

        # For the first file's token, check if it's digits or not
        example_token = tokenized[0][pos]
        example_is_digit = example_token.isdigit()

        # Collect how all files differ at this position
        all_tokens_at_pos = [t[pos] for t in tokenized]

        # If it's supposed to be a numeric token,
        # we compare the integer values to see if they differ or not.
        # If it's a non-numeric token, they must all be identical.
        if example_is_digit:
            # Parse integer values
            values = [int(x) if x.isdigit() else None for x in all_tokens_at_pos]
            # If *any* of them is None or they vary, we track that as "differences".
            # But let's see if indeed they differ across the files or not.
            if len(set(values)) > 1:
                # This token position changes among files
                num_positions.append(pos)
            else:
                # The numeric token is the same for all files, so no variation here
                pass
        else:
            # Non-digit token, must be identical across all files
            if len(set(all_tokens_at_pos)) != 1:
                raise Exception("Non-digit token differs among files. Invalid pattern.")

    # We expect exactly 1 changing numeric token position
    if len(num_positions) == 0:
        raise Exception("No numeric portion found that differs among files.")
    if len(num_positions) > 1:
        raise Exception("Multiple numeric portions found that differ. Not a single pattern.")

    varying_pos = num_positions[0]

    # -- 4) Extract the numeric values of that varying position for all sorted files,
    #        check consecutive increments and find the zero-padding width.
    numeric_values = [int(t[varying_pos]) for t in tokenized]

    # Check if consecutive differences are all +1
    for i in range(len(numeric_values) - 1):
        if numeric_values[i + 1] - numeric_values[i] != 1:
            raise Exception("Numeric values are not consecutive. Pattern is invalid.")

    # The "base" number is numeric_values[0], i.e. the value for n=0
    base_value = numeric_values[0]

    # The zero-padding width is based on the first file's numeric token
    zero_padding_width = len(tokenized[0][varying_pos])

    # -- 5) Construct the function that, given n, returns the enumerated filename.
    #        We'll verify it against the original sorted list as well.
    def generate_filename(n):
        # Rebuild the token array from the first file's tokens,
        # except we replace the one numeric token with (base_value + n) zero-padded.
        new_tokens = tokenized[0][:]

        new_int_value = base_value + n
        # zero-pad with the discovered width
        new_str_value = str(new_int_value).zfill(zero_padding_width)

        # Replace the numeric position
        new_tokens[varying_pos] = new_str_value

        # Join all tokens back into a string
        return "".join(new_tokens)

    # -- 6) Verify that generate_filename(i) reproduces the sorted list exactly
    #        for i in [0..len(sorted_files)-1].
    for i in range(len(sorted_files)):
        candidate = generate_filename(i)
        if candidate != sorted_files[i]:
            raise Exception(
                "Verification failed. The generated pattern does not match the input list."
            )

    # If we get here, everything is good. Return the generator function.
    return generate_filename


class RankStateIterable:
    """Iterates the SavableDatasetCheckpoints of mulitple ranks in a round-robin fashion."""

    def __init__(self, state_files: List[EPath]):
        state_file_names = [state_file.name for state_file in state_files]

        self.file_pattern_func = detect_and_replicate_pattern(state_file_names)
        self.num_states = len(state_files)

        # First open the first one to figure out if this is a global checkpoint or not
        first_state = torch.load(str(state_files[0]), weights_only=False)

        if isinstance(first_state, dict) and "dataloader_state_dict" in first_state:
            self.megatron_style = True
            first_state = first_state["dataloader_state_dict"]
        else:
            self.megatron_style = False

        if isinstance(first_state, SavableDataLoaderState):
            if self.megatron_style:
                self.rank_states = [first_state] + [
                    torch.load(str(state_file), weights_only=False)["dataloader_state_dict"]
                    for state_file in state_files[1:]
                ]
            else:
                self.rank_states = [first_state] + [
                    torch.load(str(state_file), weights_only=False)
                    for state_file in state_files[1:]
                ]
            self.is_global_checkpoint = False
        elif isinstance(first_state, list):
            assert len(state_files) == 1, "Global checkpoint must contain exactly one file"
            assert all(isinstance(state, SavableDataLoaderState) for state in first_state)
            self.rank_states = first_state
            self.is_global_checkpoint = True
        else:
            raise ValueError(f"Unknown checkpoint type: {type(first_state)}")

        self.rank_cur_worker = [0] * len(self.rank_states)
        self.rank_worker_offset = [state.next_worker_id for state in self.rank_states]

        self.rank_num_workers = [len(state.worker_states) for state in self.rank_states]
        assert all(
            self.rank_num_workers[0] == num_workers for num_workers in self.rank_num_workers
        ), "All ranks must have the same number of workers."

    def write_new_states_to_folder(
        self, output_folder: EPath, new_states: List[SavableDataLoaderState]
    ):
        for rank_idx, rank_state in enumerate(new_states):
            output_file = output_folder / self.file_pattern_func(rank_idx)
            if self.megatron_style:
                torch.save(
                    {"dataloader_state_dict": rank_state},
                    str(output_file),
                )
            else:
                torch.save(rank_state, str(output_file))

    def get_num_ranks(self):
        return len(self.rank_states)

    def get_num_workers(self):
        return self.rank_num_workers[0]

    def get_micro_batch_size(self):
        return self.rank_states[0].micro_batch_size

    def __iter__(self):
        """Iterates the SavableDatasetCheckpoints of mulitple ranks in a round-robin fashion."""
        for rank, state in enumerate(self.rank_states):
            for worker_state in state.worker_states:
                yield worker_state


@click.command(name="redist")
@click.argument(
    "input_files",
    nargs=-1,
    type=click.Path(file_okay=True, dir_okay=False, exists=True, path_type=EPath),
    required=True,
)
@click.argument(
    "output_path",
    type=click.Path(file_okay=False, dir_okay=True, path_type=EPath),
)
@click.option(
    "--new-world-size", type=int, help="Number of ranks to redistribute to", required=False
)
def command_redist(
    input_files: List[EPath], output_path: EPath, new_world_size: Optional[int] = None
):
    """Redistribute a checkpoint.

    Read checkpoint files from INPUT_FILES and redistribute them for a new
    number of ranks. Write the output to OUTPUT_PATH."""

    # Verify input files
    if not input_files:
        raise click.ClickException("No input files provided")

    input_file_list = sorted(input_files, key=lambda x: natural_sort_key(x.name))

    click.echo(f"Processing {len(input_file_list)} checkpoint files")

    # Determine if we're processing a single global checkpoint or multiple rank files
    rsi = RankStateIterable(input_file_list)

    if not rsi.rank_states:
        raise click.ClickException("No valid checkpoint states found")

    if new_world_size is None:
        click.echo(f"Current DP world size: {rsi.get_num_ranks()}")
        click.echo(f"Current number of workers per DP rank: {rsi.get_num_workers()}")
        new_world_size = click.prompt("Please enter the new DP world size", type=int)
        assert isinstance(new_world_size, int)

    if new_world_size <= 0:
        raise click.ClickException("New world size must be greater than 0")

    total_num_workers = rsi.get_num_workers() * rsi.get_num_ranks()
    assert total_num_workers % new_world_size == 0, (
        "New DP world size must be a multiple of the current DP world size"
    )
    new_workers_per_rank = total_num_workers // new_world_size

    # Ensure output directory exists
    output_path.mkdir(exist_ok=True, parents=True)

    new_rank_states = [list() for _ in range(new_world_size)]
    rsi_iter = iter(rsi)
    for rank_idx in range(new_world_size):
        for _ in range(new_workers_per_rank):
            state = next(rsi_iter)
            new_rank_states[rank_idx].append(state)

    assert all(
        len(new_rank_states[0]) == len(new_rank_states[rank]) for rank in range(1, new_world_size)
    ), "All ranks must have the same number of workers, also for the new distribution."

    new_states = [
        SavableDataLoaderState(
            worker_states=new_rank_state,
            next_worker_id=0,  # Reset the next worker ID
            micro_batch_size=rsi.get_micro_batch_size(),
        )
        for new_rank_state in new_rank_states
    ]

    # Save the redistributed checkpoint
    if rsi.is_global_checkpoint:
        # Save as a single global checkpoint file
        output_file = output_path / input_file_list[0].name
        torch.save(new_states, str(output_file))
        click.echo(f"Saved global checkpoint to {output_file}")
    else:
        rsi.write_new_states_to_folder(output_path, new_states)

        click.echo(f"Saved {new_world_size} rank checkpoint files to {output_path}")


@click.command(name="info")
@click.argument(
    "input_files",
    nargs=-1,
    type=click.Path(file_okay=True, dir_okay=False, exists=True, path_type=EPath),
    required=True,
)
def command_info(input_files: List[EPath]):
    """Display information about a checkpoint.

    Read a checkpoint from CHECKPOINT_PATH (either a single file or directory with *.pt files)
    and display information about it.
    """

    # Load the checkpoint(s)
    rsi = RankStateIterable(input_files)

    # Display basic information
    if rsi.is_global_checkpoint:
        click.echo("Checkpoint type: Global checkpoint")
    else:
        click.echo("Checkpoint type: Per-rank checkpoint files")

    click.echo(f"Number of DP ranks: {rsi.get_num_ranks()}")
    click.echo(f"Number of workers per DP rank: {rsi.get_num_workers()}")

    # Additional detailed information
    click.echo("\nDetailed information:")
    for rank_idx, state in enumerate(rsi.rank_states):
        if rsi.is_global_checkpoint:
            click.echo(f"  Rank {rank_idx}:")
        else:
            click.echo(f"  Rank {rank_idx} ({input_files[rank_idx].name}):")
        click.echo(f"    Next worker ID: {state.next_worker_id}")
        click.echo(f"    Number of worker states: {len(state.worker_states)}")


@click.group(
    name="checkpoint",
    context_settings=dict(help_option_names=["-h", "--help"]),
    invoke_without_command=True,
)
@click.pass_context
def command(ctx):
    """Tools for energon checkpoints."""

    # This is needed to show help if no subcommand is provided
    if ctx.invoked_subcommand is None:
        click.echo(command.get_help(ctx))


command.add_command(command_redist)
command.add_command(command_info)

if __name__ == "__main__":
    command()
