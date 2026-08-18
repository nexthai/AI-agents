
# Transformer Model Implementation

Implemented the original encoder-decoder Transformer architecture in PyTorch, including scaled dot-product attention and multi-head self-attention.

- Built sinusoidal positional encoding, position-wise feed-forward networks, residual connections, dropout, layer normalization, and vocabulary projection.

- Implemented encoder self-attention, decoder masked self-attention, encoder-decoder cross-attention, padding masks, and autoregressive causal masks.

- Constructed configurable encoder and decoder stacks supporting multiple layers, attention heads, hidden dimensions, vocabulary sizes, and sequence lengths.

- Validated tensor dimensions and end-to-end forward propagation using a six-layer, eight-head Transformer configuration.
