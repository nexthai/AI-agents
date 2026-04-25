
# Transformer Model Implementation

This project implements a basic Transformer architecture in PyTorch. It includes the core building blocks of the original encoder-decoder Transformer model, including multi-head attention, positional encoding, encoder layers, decoder layers, masking logic, and final vocabulary projection.

The implementation is designed to demonstrate how a sequence-to-sequence Transformer processes source and target token sequences and produces token-level prediction logits over the target vocabulary.

## Functionality Overview

The model takes two input sequences:

- `src`: the source sequence, usually representing the input sentence or input token IDs
- `tgt`: the target sequence, usually representing the decoder input token IDs

The Transformer encodes the source sequence, decodes the target sequence with access to the encoder output, and produces an output tensor with shape:

```text
(batch_size, target_sequence_length, target_vocabulary_size)
```

Each position in the output contains logits over the target vocabulary, which can be used for token prediction during training or inference.

## Main Components

### MultiHeadAttention

The `MultiHeadAttention` module implements scaled dot-product attention across multiple attention heads.

It performs the following operations:

1. Projects the input tensors into Query, Key, and Value representations.
2. Splits the projected tensors into multiple attention heads.
3. Computes scaled dot-product attention for each head.
4. Applies an optional mask to prevent attending to padding tokens or future tokens.
5. Combines all attention heads back into a single tensor.
6. Applies a final linear projection.

This module is used in both the encoder and decoder.

In the encoder, it is used as self-attention, where `Q`, `K`, and `V` all come from the same input sequence.

In the decoder, it is used in two ways:

- Masked self-attention over the target sequence
- Cross-attention over the encoder output

## PositionWiseFeedForward

The `PositionWiseFeedForward` module applies a feed-forward neural network independently to each token position.

It consists of:

1. A linear layer that expands the hidden dimension from `d_model` to `d_ff`
2. A ReLU activation
3. Dropout
4. A second linear layer that projects the representation back from `d_ff` to `d_model`

This module helps the model transform each token representation after attention has mixed contextual information across the sequence.

## PositionalEncoding

The `PositionalEncoding` module adds position information to token embeddings.

Since the Transformer does not use recurrence or convolution, it needs an explicit way to represent token order. This implementation uses sinusoidal positional encoding.

The positional encoding matrix is created using sine functions for even dimensions and cosine functions for odd dimensions. These encodings are added directly to the token embeddings before the sequence enters the encoder or decoder layers.

The positional encoding is registered as a buffer, meaning it is not treated as a trainable parameter but still moves with the model when transferred to a device such as CPU or GPU.

## EncoderLayer

The `EncoderLayer` represents one Transformer encoder block.

Each encoder layer contains:

1. Multi-head self-attention
2. Residual connection
3. Layer normalization
4. Position-wise feed-forward network
5. Another residual connection
6. Another layer normalization

The encoder layer takes the embedded source sequence and allows each token to attend to other valid source tokens.

Padding positions are masked so that the model does not attend to meaningless padding tokens.

## DecoderLayer

The `DecoderLayer` represents one Transformer decoder block.

Each decoder layer contains:

1. Masked multi-head self-attention over the target sequence
2. Residual connection and layer normalization
3. Cross-attention over the encoder output
4. Residual connection and layer normalization
5. Position-wise feed-forward network
6. Final residual connection and layer normalization

The masked self-attention prevents each target token from seeing future target tokens. This is necessary for autoregressive generation, where the model should only use previous tokens when predicting the next token.

The cross-attention layer allows the decoder to attend to the encoded source sequence.

## Encoder

The `Encoder` converts source token IDs into contextual hidden representations.

It performs the following steps:

1. Converts source token IDs into embeddings.
2. Adds positional encoding.
3. Passes the result through multiple encoder layers.
4. Applies a final layer normalization.

The output of the encoder is passed to the decoder and serves as the memory representation of the source sequence.

## Decoder

The `Decoder` converts target token IDs into contextual decoder representations.

It performs the following steps:

1. Converts target token IDs into embeddings.
2. Adds positional encoding.
3. Passes the result through multiple decoder layers.
4. Applies a final layer normalization.

The decoder uses both the target sequence and the encoder output to generate representations for target-side prediction.

## Transformer

The `Transformer` class combines the encoder, decoder, and final output projection.

Its forward pass includes:

1. Generating source and target masks
2. Encoding the source sequence
3. Decoding the target sequence using the encoder output
4. Projecting decoder hidden states to the target vocabulary size

The final output is a tensor of logits with shape:

```text
(batch_size, target_sequence_length, target_vocabulary_size)
```

These logits can be used with a loss function such as cross-entropy loss during training.

## Masking Behavior

The model includes two types of masks.

### Source Mask

The source mask prevents the encoder and decoder cross-attention from attending to padding tokens in the source sequence.

Padding tokens are assumed to have token ID `0`.

The source mask has shape:

```text
(batch_size, 1, 1, source_sequence_length)
```

### Target Mask

The target mask combines two masking strategies:

1. Padding mask: prevents attention to padding tokens in the target sequence.
2. Subsequent mask: prevents each target position from attending to future target positions.

This ensures that during decoding, each target token can only attend to previous or current target tokens.

The target mask has shape:

```text
(batch_size, 1, target_sequence_length, target_sequence_length)
```

## Example Behavior

The demo code creates a Transformer with the following configuration:

```text
source vocabulary size: 5000
target vocabulary size: 5000
model dimension: 512
number of layers: 6
number of attention heads: 8
feed-forward hidden dimension: 2048
dropout: 0.1
maximum sequence length: 100
```

It then creates random source and target token sequences:

```text
src shape: (2, 10)
tgt shape: (2, 12)
```

After passing these inputs through the model, the output shape is:

```text
torch.Size([2, 12, 5000])
```

This means:

- There are 2 samples in the batch.
- The target sequence length is 12.
- For each target position, the model outputs logits over 5000 target vocabulary tokens.

## Data Flow

The full data flow is:

```text
Source token IDs
    -> Source embedding
    -> Positional encoding
    -> Encoder layers
    -> Encoder output

Target token IDs
    -> Target embedding
    -> Positional encoding
    -> Decoder layers with encoder output
    -> Final linear layer
    -> Vocabulary logits
```

## Notes

This implementation is a simplified educational Transformer model. It focuses on the core architecture and forward-pass mechanics rather than training utilities, dataset handling, inference decoding strategies, checkpointing, or production-level optimization.

It is useful for understanding how the main components of a Transformer interact with each other, especially:

- Multi-head attention
- Encoder-decoder structure
- Residual connections
- Layer normalization
- Positional encoding
- Padding masks
- Causal target masks
