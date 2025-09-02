import pacmap
import numpy as np
df_scaled = np.random.random(size=(42359, 12))
embedding1 = pacmap.PaCMAP(n_components=2, n_neighbors=10, MN_ratio=0.5, FP_ratio=2.0,
random_state=20, save_tree=False,
intermediate=True,
verbose=1)

X_transformed1 = embedding1.fit_transform(df_scaled, init="pca")

