


def get_all_bounds(binary:bytes):
  head = header(binary)
  if head.label_format == LabelFormat.FLAT:
    return z_range_for_label_flat(binary, label)
  elif head.label_format == LabelFormat.PINS_VARIABLE_WIDTH:
    return z_range_for_label_condensed_pins(binary, label)
  else:
    raise ValueError("Label format not supported.")

def get_all_bounds_flat(binary:bytes, label:int) -> Dict[int,Tuple[int,int,int,int,int,int]]:
  head = header(binary)
  labels_binary = raw_labels(binary)
 
  num_labels = int.from_bytes(labels_binary[:8], 'little')

  if num_labels == 0:
  	return {}

  offset = 8
  uniq = np.frombuffer(
    labels_binary,
    offset=offset,
    count=num_labels,
    dtype=head.stored_dtype
  )
  try:
    label = np.asarray(label, dtype=uniq.dtype)
    idx = np.searchsorted(uniq, label)
  except OverflowError:
    idx = -1
    
  if idx < 0 or idx >= uniq.size or uniq[idx] != label:
    return (-1, -1)

  offset += num_labels * head.stored_data_width
  next_offset = offset + head.num_grids() * head.component_width()
  dtype = width2dtype[head.component_width()]

  components_per_grid = np.frombuffer(
    labels_binary,
    offset=offset,
    count=head.num_grids(), 
    dtype=dtype
  )
  components_per_grid = np.cumsum(components_per_grid)

  offset = next_offset
 
  dtype = compute_dtype(num_labels)
  cc_labels = np.frombuffer(labels_binary, offset=offset, dtype=dtype)

  cc_idxs = fastcrackle.index_range(cc_labels, idx)

  if cc_idxs.size == 0:
    return (-1, -1)

  min_cc = cc_idxs[0]
  max_cc = cc_idxs[-1]

  z_start = 0
  z_end = head.sz - 1

  for z in range(head.sz):
    if components_per_grid[z] >= min_cc:
      z_start = z
      break

  for z in range(head.sz - 1, -1, -1):
    if components_per_grid[z] <= max_cc:
      z_end = z + 1
      break

  return (int(z_start), int(z_end+1))
