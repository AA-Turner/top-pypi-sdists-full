import numpy as np
import networkx as nx
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
from scipy import sparse
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from sklearn.neighbors import NearestNeighbors, KDTree
from scipy.sparse import csr_matrix, lil_matrix, diags
from scipy.sparse.linalg import eigs
from scipy.sparse.csgraph import dijkstra
import heapq
from typing import Tuple, List, Dict, Optional, Union
import warnings
warnings.filterwarnings('ignore')




class ClusterNetworkBuilder:
    """
    基于KNN的聚类中心网络构建器
    
    算法步骤：
    1. 建立聚类中心c到数据点x的knn网络H
    2. 基于H建立聚类中心c的网络G
       - 如果两个聚类中心c1可以经过某个数据点到达c2，则c1和c2建立边
       - 边的权重由中介数据点的数量决定
       - 中介数据点的比重越大，边的权重越大
    """
    
    def __init__(self, 
                 k_data_to_centers=5,      # 每个数据点连接到多少个聚类中心
                 k_centers_to_data=10,     # 每个聚类中心连接到多少个数据点
                 weight_method='count',     # 权重计算方法: 'count', 'proportion', 'weighted'
                 min_edge_weight=0.01,     # 最小边权重
                 normalize_weights=True,   # 是否归一化权重
                 symmetric=True,           # 是否创建对称边
                 use_jaccard=False):       # 是否使用Jaccard相似度
        """
        参数:
        k_data_to_centers: 每个数据点连接到k个最近的聚类中心
        k_centers_to_data: 每个聚类中心连接到k个最近的数据点
        weight_method: 权重计算方法
            - 'count': 使用中介数据点的数量
            - 'proportion': 使用中介数据点的比例
            - 'weighted': 使用加权计数
        """
        self.k_data_to_centers = k_data_to_centers
        self.k_centers_to_data = k_centers_to_data
        self.weight_method = weight_method
        self.min_edge_weight = min_edge_weight
        self.normalize_weights = normalize_weights
        self.symmetric = symmetric
        self.use_jaccard = use_jaccard
        
    def build_network(self, x, c, metric='euclidean', return_details=False):
        """
        构建聚类中心网络
        
        参数:
        x: 数据点 (n_samples, n_features)
        c: 聚类中心 (n_clusters, n_features)
        metric: 距离度量
        return_details: 是否返回详细中间结果
        
        返回:
        G: 聚类中心网络
        如果return_details=True，还返回(H, edge_weights_dict, data_assignments)
        """
        n_samples = x.shape[0]
        n_clusters = c.shape[0]
        
        # 步骤1: 构建KNN网络H（二部图）
        H, data_assignments = self._build_knn_bipartite(x, c, metric)
        
        # 步骤2: 基于H构建聚类中心网络G
        G, edge_weights_dict = self._build_cluster_network_from_bipartite(
            H, n_clusters, n_samples
        )
        
        # 为节点添加属性
        self._add_node_attributes(G, c, data_assignments, n_samples)
        
        if return_details:
            return G, H, edge_weights_dict, data_assignments
        return G
    
    def _build_knn_bipartite(self, x, c, metric):
        """构建数据点和聚类中心的KNN二部图H"""
        n_samples = x.shape[0]
        n_clusters = c.shape[0]
        
        # 创建二部图
        H = nx.Graph()
        
        # 添加节点
        # 数据点节点: 前缀'd_'，如'd_0', 'd_1', ...
        for i in range(n_samples):
            H.add_node(f'd_{i}', type='data', index=i, features=x[i])
        
        # 聚类中心节点: 前缀'c_'，如'c_0', 'c_1', ...
        for j in range(n_clusters):
            H.add_node(f'c_{j}', type='cluster', index=j, center=c[j])
        
        # 1. 数据点到聚类中心的连接
        if self.k_data_to_centers > 0:
            # 计算每个数据点到所有聚类中心的距离
            data_to_center_dists = cdist(x, c, metric=metric)
            
            # 为每个数据点找到k个最近的聚类中心
            k1 = min(self.k_data_to_centers, n_clusters)
            for i in range(n_samples):
                # 找到最近的k1个聚类中心
                if k1 < n_clusters:
                    # 使用argpartition提高效率
                    nearest = np.argpartition(data_to_center_dists[i], k1)[:k1]
                else:
                    nearest = np.arange(n_clusters)
                
                for j in nearest:
                    distance = data_to_center_dists[i, j]
                    H.add_edge(f'd_{i}', f'c_{j}', 
                              #weight=1.0/(1.0 + distance),
                              weight=np.exp(-distance),
                              distance=distance,
                              type='data_to_center')
        
        # 2. 聚类中心到数据点的连接
        if self.k_centers_to_data > 0:
            # 计算每个聚类中心到所有数据点的距离
            center_to_data_dists = cdist(c, x, metric=metric)
            
            # 为每个聚类中心找到k个最近的数据点
            k2 = min(self.k_centers_to_data, n_samples)
            for j in range(n_clusters):
                if k2 < n_samples:
                    nearest = np.argpartition(center_to_data_dists[j], k2)[:k2]
                else:
                    nearest = np.arange(n_samples)
                
                for i in nearest:
                    distance = center_to_data_dists[j, i]
                    H.add_edge(f'c_{j}', f'd_{i}',
                              #weight=1.0/(1.0 + distance),
                              weight=np.exp(-distance),
                              distance=distance,
                              type='center_to_data')
        
        # 创建数据点分配矩阵
        data_assignments = self._create_data_assignments(H, n_samples, n_clusters)
        
        return H, data_assignments
    
    def _create_data_assignments(self, H, n_samples, n_clusters):
        """从二部图创建数据点分配矩阵"""
        assignments = np.zeros((n_samples, n_clusters))
        
        for i in range(n_samples):
            data_node = f'd_{i}'
            if data_node in H:
                # 获取连接到这个数据点的所有聚类中心
                cluster_neighbors = [n for n in H.neighbors(data_node) 
                                   if n.startswith('c_')]
                
                for cluster_node in cluster_neighbors:
                    j = int(cluster_node.split('_')[1])
                    # 使用边的权重作为分配权重
                    weight = H[data_node][cluster_node].get('weight', 1.0)
                    assignments[i, j] = weight
        
        # 归一化每行的分配（使每行和为1）
        row_sums = assignments.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # 避免除零
        assignments = assignments / row_sums
        
        return assignments
    
    def _build_cluster_network_from_bipartite(self, H, n_clusters, n_samples):
        """从二部图构建聚类中心网络"""
        G = nx.Graph()
        
        # 添加聚类中心节点
        for j in range(n_clusters):
            G.add_node(j, index=j)
        
        # 计算边权重
        edge_weights = defaultdict(float)
        
        # 方法1: 通过数据点连接聚类中心
        for i in range(n_samples):
            data_node = f'd_{i}'
            if data_node in H:
                # 获取连接到这个数据点的所有聚类中心
                cluster_neighbors = [n for n in H.neighbors(data_node) 
                                   if n.startswith('c_')]
                cluster_indices = [int(n.split('_')[1]) for n in cluster_neighbors]
                
                # 为每对聚类中心添加权重
                for idx1, c1 in enumerate(cluster_indices):
                    for c2 in cluster_indices[idx1+1:]:
                        # 这个数据点同时连接到c1和c2
                        edge_key = tuple(sorted((c1, c2)))
                        
                        # 计算这个数据点对这条边的贡献
                        weight_c1 = H[data_node][f'c_{c1}'].get('weight', 1.0)
                        weight_c2 = H[data_node][f'c_{c2}'].get('weight', 1.0)
                        
                        if self.weight_method == 'count':
                            # 计数：每个中介数据点贡献1
                            contribution = 1.0
                        elif self.weight_method == 'weighted':
                            # 加权：使用连接权重的乘积
                            contribution = weight_c1 * weight_c2
                        else:  # 'proportion'
                            # 比例：平均权重
                            contribution = (weight_c1 + weight_c2) / 2.0
                        
                        edge_weights[edge_key] += contribution
        
        # 如果使用Jaccard相似度
        if self.use_jaccard:
            edge_weights = self._compute_jaccard_weights(H, n_clusters, edge_weights)
        
        # 归一化权重
        if self.normalize_weights and edge_weights:
            max_weight = max(edge_weights.values())
            if max_weight > 0:
                for key in edge_weights:
                    edge_weights[key] /= max_weight
        
        # 添加边到网络G
        for (c1, c2), weight in edge_weights.items():
            if weight >= self.min_edge_weight:
                G.add_edge(c1, c2, weight=weight, 
                          n_mediators=int(weight * 10))  # 估计的中介点数
        
        return G, dict(edge_weights)
    
    def _compute_jaccard_weights(self, H, n_clusters, edge_weights):
        """计算Jaccard相似度作为边权重"""
        # 计算每个聚类中心连接的数据点集合
        cluster_data_sets = {}
        for j in range(n_clusters):
            cluster_node = f'c_{j}'
            if cluster_node in H:
                data_neighbors = {n for n in H.neighbors(cluster_node) 
                                if n.startswith('d_')}
                cluster_data_sets[j] = data_neighbors
        
        # 重新计算边权重为Jaccard相似度
        jaccard_weights = {}
        clusters = list(cluster_data_sets.keys())
        
        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                c1, c2 = clusters[i], clusters[j]
                set1 = cluster_data_sets.get(c1, set())
                set2 = cluster_data_sets.get(c2, set())
                
                if set1 and set2:
                    intersection = len(set1.intersection(set2))
                    union = len(set1.union(set2))
                    jaccard = intersection / union if union > 0 else 0
                    
                    if jaccard > 0:
                        jaccard_weights[(c1, c2)] = jaccard
        
        return jaccard_weights
    
    def _add_node_attributes(self, G, c, data_assignments, n_samples):
        """为节点添加属性"""
        n_clusters = c.shape[0]
        
        for j in range(n_clusters):
            if j in G:
                # 计算分配给这个聚类的数据点
                cluster_assignments = data_assignments[:, j]
                
                # 硬分配计数（分配权重大于0.5）
                hard_count = np.sum(cluster_assignments > 0.5)
                
                # 软分配权重和
                soft_weight = np.sum(cluster_assignments)
                
                # 更新节点属性
                G.nodes[j].update({
                    'center': c[j],
                    'hard_assigned_count': hard_count,
                    'soft_assigned_weight': soft_weight,
                    'proportion': soft_weight / n_samples,
                    'avg_assignment': np.mean(cluster_assignments[cluster_assignments > 0])
                })
    



class KnnClusterNetworkBuilder:
    """
    基于KNN的聚类中心网络构建器
    
    算法：
    1. 建立聚类中心c到数据点x的knn网络H
    2. 建立数据x的knn网络M
    3. 基于H建立聚类中心c的网络G，对任何两个中心c1和c2，
       它们之间的距离定义为从其中一个中心出发经过网络M到达另一个中心的最短距离d，
       c1和c2之间的边的权重定义为exp(-d/t)，t为temperature
    """
    
    def __init__(self, 
                 k_data: int = 5,
                 k_centers: int = 15,
                 temperature: float = 1.0,
                 metric: str = 'euclidean',
                 algorithm: str = 'auto',
                 directed: bool = False,
                 weight_strategy: str = 'distance',
                 symmetric: bool = True,
                 use_sparse: bool = True):
        """
        参数:
        k_data: 数据点KNN的k值
        k_centers: 聚类中心到数据点的KNN的k值
        temperature: 距离到权重的转换温度
        metric: 距离度量 ('euclidean', 'cosine', 'manhattan', 等)
        algorithm: KNN算法 ('auto', 'kd_tree', 'ball_tree', 'brute')
        directed: 是否构建有向图
        weight_strategy: 权重策略 ('distance', 'shared', 'combined')
        symmetric: 是否强制对称（无向图）
        use_sparse: 是否使用稀疏矩阵加速
        """
        self.k_data = k_data
        self.k_centers = k_centers
        self.temperature = temperature
        self.metric = metric
        self.algorithm = algorithm
        self.directed = directed
        self.weight_strategy = weight_strategy
        self.symmetric = symmetric
        self.use_sparse = use_sparse
        
        # 缓存
        self._H = None  # 中心到数据的KNN图
        self._M = None  # 数据的KNN图
        self._G = None  # 最终的中心网络
        self._shortest_paths = None  # 最短路径缓存
        
    def build_network(self, 
                     x: np.ndarray, 
                     c: np.ndarray,
                     return_intermediate: bool = False) -> nx.Graph:
        """
        构建聚类中心网络
        
        参数:
        x: 数据点，形状 (n_samples, n_features)
        c: 聚类中心，形状 (n_clusters, n_features)
        return_intermediate: 是否返回中间图
        
        返回:
        G: 聚类中心网络
        如果return_intermediate为True，也返回(H, M)
        """        
        # 1. 构建数据点的KNN图 M
        M = self._build_data_knn_graph(x)
        
        # 2. 构建聚类中心到数据的KNN图 H
        H = self._build_centers_to_data_knn_graph(x, c)
        
        # 3. 构建最终的聚类中心网络 G
        G = self._build_final_network(x, c, H, M)
        
        # 保存中间结果
        self._M = M
        self._H = H
        self._G = G
        
        if return_intermediate:
            return G, H, M
        return G
    
    def _build_data_knn_graph(self, x: np.ndarray) -> nx.Graph:
        """构建数据点的KNN图 M"""
        n_samples = x.shape[0]
        
        # 构建KNN
        k_actual = min(self.k_data, n_samples - 1)
        if k_actual < 1:
            # 如果样本太少，构建完全图
            M = nx.complete_graph(n_samples)
            # 添加距离作为边权重
            distances = cdist(x, x, self.metric)
            for i in range(n_samples):
                for j in range(i+1, n_samples):
                    M[i][j]['weight'] = distances[i, j]
            return M
        
        # 使用sklearn的KNN
        nbrs = NearestNeighbors(
            n_neighbors=k_actual + 1,  # +1 因为包含自己
            algorithm=self.algorithm,
            metric=self.metric
        ).fit(x)
        
        distances, indices = nbrs.kneighbors(x)
        
        # 构建图
        if self.directed:
            M = nx.DiGraph()
        else:
            M = nx.Graph()
        
        # 添加节点
        M.add_nodes_from(range(n_samples))
        
        # 添加边
        for i in range(n_samples):
            # 获取邻居（排除自己）
            neighbors = indices[i, 1:]  # 第0个是自己
            neighbor_distances = distances[i, 1:]
            
            for j, dist in zip(neighbors, neighbor_distances):
                if not self.directed and i > j:
                    # 对于无向图，避免重复添加
                    if M.has_edge(i, j):
                        continue
                
                # 根据权重策略添加边权重
                if self.weight_strategy == 'distance':
                    weight = dist
                elif self.weight_strategy == 'shared':
                    # 共享邻居数量
                    weight = 1.0
                elif self.weight_strategy == 'combined':
                    weight = dist
                else:
                    weight = 1.0
                
                M.add_edge(i, j, weight=weight, distance=dist)
        
        return M
    
    def _build_centers_to_data_knn_graph(self, x: np.ndarray, c: np.ndarray) -> nx.Graph:
        """构建聚类中心到数据的KNN图 H"""
        n_samples = x.shape[0]
        n_clusters = c.shape[0]
        
        # 构建KNN：从中心到数据
        k_actual = min(self.k_centers, n_samples)
        
        nbrs = NearestNeighbors(
            n_neighbors=k_actual,
            algorithm=self.algorithm,
            metric=self.metric
        ).fit(x)
        
        distances, indices = nbrs.kneighbors(c)
        
        # 构建二分图 H
        H = nx.Graph()
        
        # 添加节点
        # 聚类中心节点：0 到 n_clusters-1
        # 数据点节点：n_clusters 到 n_clusters + n_samples - 1
        H.add_nodes_from(range(n_clusters + n_samples))
        
        # 标记节点类型
        for i in range(n_clusters):
            H.nodes[i]['type'] = 'center'
            H.nodes[i]['center_id'] = i
            H.nodes[i]['original_index'] = i
        
        for i in range(n_samples):
            node_id = n_clusters + i
            H.nodes[node_id]['type'] = 'data'
            H.nodes[node_id]['data_id'] = i
            H.nodes[node_id]['original_index'] = i
        
        # 添加边：中心到数据
        for center_idx in range(n_clusters):
            data_indices = indices[center_idx]
            data_distances = distances[center_idx]
            
            for data_idx, dist in zip(data_indices, data_distances):
                data_node_id = n_clusters + data_idx
                H.add_edge(center_idx, data_node_id, 
                          weight=dist, 
                          distance=dist,
                          center_id=center_idx,
                          data_id=data_idx)
        
        return H
    
    def _build_final_network(self, 
                           x: np.ndarray, 
                           c: np.ndarray,
                           H: nx.Graph,
                           M: nx.Graph) -> nx.Graph:
        """构建最终的聚类中心网络 G"""
        n_clusters = c.shape[0]
        n_samples = x.shape[0]
        
        # 创建最终的网络
        G = nx.Graph()
        
        # 添加聚类中心节点
        for i in range(n_clusters):
            G.add_node(i, center=c[i], index=i)
        
        # 预计算数据点之间的最短路径
        data_shortest_paths = self._compute_data_shortest_paths(M, n_samples)
        
        # 计算中心之间的最短路径距离        
        # 获取H中每个中心连接的数据点
        center_to_data = {}
        for center_idx in range(n_clusters):
            connected_data = []
            for neighbor in H.neighbors(center_idx):
                if H.nodes[neighbor]['type'] == 'data':
                    data_id = H.nodes[neighbor]['data_id']
                    weight = H[center_idx][neighbor]['weight']
                    connected_data.append((data_id, weight))
            center_to_data[center_idx] = connected_data
        
        # 计算所有中心对之间的最短路径
        center_distances = np.full((n_clusters, n_clusters), np.inf)
        center_paths = {}
        
        for i in range(n_clusters):
            center_distances[i, i] = 0
            for j in range(i+1, n_clusters):
                # 计算从中心i到中心j的最短路径
                distance, path = self._compute_center_to_center_distance(
                    i, j, center_to_data, data_shortest_paths, H
                )
                
                if distance < np.inf:
                    center_distances[i, j] = distance
                    center_distances[j, i] = distance
                    center_paths[(i, j)] = path
                    center_paths[(j, i)] = list(reversed(path))
        
        # 添加边到网络G
        edges_added = 0
        
        for i in range(n_clusters):
            for j in range(i+1, n_clusters):
                distance = center_distances[i, j]
                
                if distance < np.inf:
                    # 计算边权重: exp(-d/t)
                    weight = np.exp(-distance / self.temperature)
                    
                    # 获取路径信息
                    path_info = center_paths.get((i, j), [])
                    
                    # 添加边
                    G.add_edge(i, j, 
                              weight=weight,
                              distance=distance,
                              raw_distance=distance,
                              temperature=self.temperature,
                              path=path_info)
                    
                    edges_added += 1
                
        # 如果是对称的，确保权重对称
        if self.symmetric and not self.directed:
            for i, j in G.edges():
                if G[i][j]['weight'] != G[j][i]['weight']:
                    # 取平均值
                    avg_weight = (G[i][j]['weight'] + G[j][i]['weight']) / 2
                    G[i][j]['weight'] = avg_weight
                    G[j][i]['weight'] = avg_weight
        
        return G
    
    def _compute_data_shortest_paths(self, M: nx.Graph, n_samples: int) -> np.ndarray:
        """预计算数据点之间的最短路径距离"""
        
        if self.use_sparse and n_samples > 100:
            # 使用稀疏矩阵和Dijkstra算法
            # 创建邻接矩阵
            adj_matrix = np.full((n_samples, n_samples), np.inf)
            np.fill_diagonal(adj_matrix, 0)
            
            for u, v, data in M.edges(data=True):
                weight = data.get('weight', 1.0)
                adj_matrix[u, v] = weight
                if not self.directed:
                    adj_matrix[v, u] = weight
            
            # 使用Dijkstra算法
            from scipy.sparse import csr_matrix
            from scipy.sparse.csgraph import dijkstra
            
            sparse_adj = csr_matrix(adj_matrix)
            distances = dijkstra(sparse_adj, directed=self.directed)
            
            return distances
        else:
            # 使用NetworkX的最短路径
            distances = np.full((n_samples, n_samples), np.inf)
            np.fill_diagonal(distances, 0)
            
            # 对于小图，使用所有对最短路径
            if n_samples < 1000:
                all_pairs = dict(nx.all_pairs_dijkstra_path_length(M, weight='weight'))
                for u in all_pairs:
                    for v, dist in all_pairs[u].items():
                        distances[u, v] = dist
            else:
                # 对于大图，只计算必要的
                warnings.warn("数据点太多，最短路径计算可能较慢")
                return None
            
            return distances
    
    def _compute_center_to_center_distance(self,
                                         center_i: int,
                                         center_j: int,
                                         center_to_data: Dict[int, List[Tuple[int, float]]],
                                         data_shortest_paths: Optional[np.ndarray],
                                         H: nx.Graph) -> Tuple[float, List]:
        """
        计算从中心i到中心j的最短路径距离
        
        路径格式: 中心i -> 数据a -> ... -> 数据b -> 中心j
        """
        data_i_list = center_to_data[center_i]  # [(data_id, weight), ...]
        data_j_list = center_to_data[center_j]  # [(data_id, weight), ...]
        
        if not data_i_list or not data_j_list:
            return np.inf, []
        
        min_distance = np.inf
        min_path = []
        
        # 遍历所有可能的起点和终点数据点
        for data_i, weight_i in data_i_list:
            for data_j, weight_j in data_j_list:
                if data_i == data_j:
                    # 同一个数据点
                    total_distance = weight_i + weight_j
                    path = [center_i, data_i, center_j]
                else:
                    # 需要计算数据点之间的最短路径
                    if data_shortest_paths is not None:
                        data_distance = data_shortest_paths[data_i, data_j]
                    else:
                        # 实时计算最短路径
                        try:
                            data_distance = nx.shortest_path_length(
                                self._M, data_i, data_j, weight='weight'
                            )
                        except nx.NetworkXNoPath:
                            continue
                    
                    if data_distance < np.inf:
                        total_distance = weight_i + data_distance + weight_j
                        path = [center_i, data_i, data_j, center_j]
                    else:
                        continue
                
                if total_distance < min_distance:
                    min_distance = total_distance
                    min_path = path
        
        return min_distance, min_path
    
    


class EdgeAllocation:
    """
    使用偏最小二乘回归(PLSR)将数据点分配到图边上的类
    """
    
    def __init__(self, n_components: int = 2, alpha: float = 0.1):
        """
        初始化
        
        参数:
        n_components: PLS回归的组件数
        alpha: 分配的平滑参数，防止过度集中在最近的点
        """
        self.n_components = n_components
        self.alpha = alpha
        self.pls = None
        self.scaler_x = StandardScaler()
        self.scaler_y = StandardScaler()
        
    def _point_to_line_distance(self, point: np.ndarray, 
                               start: np.ndarray, 
                               end: np.ndarray) -> float:
        """
        计算点到线段的距离
        
        参数:
        point: 数据点坐标
        start: 线段起点
        end: 线段终点
        
        返回:
        点到线段的距离
        """
        # 线段向量
        line_vec = end - start
        point_vec = point - start
        
        # 线段长度
        line_len = np.linalg.norm(line_vec)
        
        if line_len == 0:
            return np.linalg.norm(point - start)
        
        # 归一化的线段向量
        line_unit = line_vec / line_len
        
        # 点在线段上的投影长度
        proj_length = np.dot(point_vec, line_unit)
        
        if proj_length < 0:
            # 投影在线段起点之前
            return np.linalg.norm(point - start)
        elif proj_length > line_len:
            # 投影在线段终点之后
            return np.linalg.norm(point - end)
        else:
            # 投影在线段上
            projection = start + proj_length * line_unit
            return np.linalg.norm(point - projection)
    
    def fit_transform(self, x: np.ndarray, c: np.ndarray, G: nx.Graph, metric: str='cosine') -> Dict[Tuple, float]:
        """
        将数据点分配到图的边上，返回边的权重（分配到的数据比例）
        
        参数:
        x: 数据点，形状 (n_samples, n_features)
        c: 聚类中心，形状 (n_clusters, n_features)
        G: 图，节点为聚类中心索引，边表示连接
        
        返回:
        边的权重字典，键为边(节点i, 节点j)，值为分配的权重
        """
        n_samples, n_features = x.shape
        n_clusters = c.shape[0]
        
        # 1. 准备PLS回归数据
        # 为每个数据点创建聚类中心的软分配标签
        # 使用距离的倒数作为软标签
        distances = cdist(x, c, metric=metric)
        #soft_labels = 1.0 / (distances + 1e-10)  # 防止除零
        soft_labels = np.exp(-distances)
        soft_labels = soft_labels / soft_labels.sum(axis=1, keepdims=True)  # 归一化
        
        # 2. 拟合PLS回归模型
        x_scaled = self.scaler_x.fit_transform(x)
        y_scaled = self.scaler_y.fit_transform(soft_labels)
        
        self.pls = PLSRegression(n_components=min(self.n_components, n_features))
        self.pls.fit(x_scaled, y_scaled)
        
        # 3. 预测每个点对聚类中心的归属度
        x_scaled = self.scaler_x.transform(x)
        y_pred = self.pls.predict(x_scaled)
        y_pred = np.maximum(y_pred, 0)  # 确保非负
        y_pred = y_pred / y_pred.sum(axis=1, keepdims=True)  # 归一化
        
        # 4. 将点分配到边上
        edges = list(G.edges())
        edge_weights = {edge: 0.0 for edge in edges}
        
        for i in range(n_samples):
            point = x[i]
            cluster_probs = y_pred[i]  # 点属于每个聚类中心的概率
            
            # 对每个边计算分配权重
            edge_distances = []
            edge_probs = []
            
            for edge in edges:
                node_i, node_j = edge
                # 获取聚类中心坐标
                center_i = c[node_i]
                center_j = c[node_j]
                
                # 计算点到边的距离
                dist = self._point_to_line_distance(point, center_i, center_j)
                
                # 计算边相关的聚类中心的平均概率
                edge_prob = (cluster_probs[node_i] + cluster_probs[node_j]) / 2
                
                edge_distances.append(dist)
                edge_probs.append(edge_prob)
            
            # 将距离转换为相似度（使用高斯核）
            edge_distances = np.array(edge_distances)
            edge_probs = np.array(edge_probs)
            
            # 计算边对点的吸引力
            # 结合距离相似度和聚类概率
            similarities = np.exp(-self.alpha * edge_distances) * edge_probs
            
            # 归一化为分配权重
            if similarities.sum() > 0:
                edge_weights_for_point = similarities / similarities.sum()
            else:
                edge_weights_for_point = np.ones(len(edges)) / len(edges)
            
            # 累加权重
            for (edge, weight) in zip(edges, edge_weights_for_point):
                edge_weights[edge] += weight / n_samples  # 平均到每个点
        
        return edge_weights
    

def visualize_network(G, c=None, node_size_attr='weight', node_size_scale=5000, edge_size_scale=30, figsize=(12, 10)):
    """可视化聚类中心网络"""
    fig, ax1 = plt.subplots(1, 1, figsize=figsize)
    
    # 位置布局（如果提供了聚类中心坐标，使用它们；否则使用力导向布局）
    if c is not None and c.shape[1] >= 2:
        # 使用前两个维度作为位置
        pos = {i: (c[i, 0], c[i, 1]) for i in G.nodes()}
        
        # 如果只有1D，添加一个虚拟维度
        if c.shape[1] == 1:
            pos = {i: (c[i, 0], i) for i in G.nodes()}
    else:
        pos = nx.spring_layout(G, seed=42, weight='weight')
    
    # 节点大小基于权重
    node_weights = [G.nodes[node][node_size_attr] for node in G.nodes()]
    node_sizes = [node_size_scale * w for w in node_weights]
    
    # 节点颜色基于权重
    node_colors = node_weights
    
    # 边宽度基于权重
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    edge_widths = [edge_size_scale * w for w in edge_weights]
    
    # 绘制网络
    nodes = nx.draw_networkx_nodes(G, pos, 
                                  node_size=node_sizes,
                                  node_color=node_colors,
                                  cmap='viridis',
                                  alpha=0.8,
                                  edgecolors='black',
                                  linewidths=1,
                                  ax=ax1)
    
    nx.draw_networkx_edges(G, pos,
                          width=edge_widths,
                          alpha=0.6,
                          edge_color='gray',
                          ax=ax1)
    
    nx.draw_networkx_labels(G, pos,
                           font_size=10,
                           font_weight='bold',
                           ax=ax1)
    
    # 添加颜色条
    sm = plt.cm.ScalarMappable(cmap='viridis', 
                               norm=plt.Normalize(vmin=min(node_colors), 
                                                  vmax=max(node_colors)))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax1, shrink=0.8)
    cbar.set_label('Node Weight')
    
    ax1.axis('off')
    
    plt.tight_layout()
    plt.show()




def visualize_network_interactive(G, c=None, node_size_scale=5000, edge_size_scale=30, 
                                 figsize=(1000, 800), show_labels=True, title=""):
    """
    使用Plotly的交互式可视化聚类中心网络
    
    参数:
    G: NetworkX图
    c: 聚类中心坐标 (n_clusters, n_features)
    node_size_scale: 节点大小缩放因子
    edge_size_scale: 边宽度缩放因子
    figsize: 图形大小 (宽度, 高度)
    show_labels: 是否显示节点标签
    title: 图形标题
    
    返回:
    Plotly图形对象
    """
    # 1. 计算节点位置
    if c is not None and c.shape[1] >= 2:
        # 使用前两个维度作为位置
        pos = {i: (float(c[i, 0]), float(c[i, 1])) for i in G.nodes()}
        
        # 如果只有1D，添加一个虚拟维度
        if c.shape[1] == 1:
            pos = {i: (float(c[i, 0]), float(i)) for i in G.nodes()}
    else:
        pos = nx.spring_layout(G, seed=42, weight='weight')
    
    # 2. 准备节点数据
    node_x = []
    node_y = []
    node_sizes = []
    node_colors = []
    node_labels = []
    node_hover_texts = []
    node_ids = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_ids.append(node)
        
        # 获取节点属性
        node_weight = G.nodes[node].get('weight', 1.0)
        node_sizes.append(node_size_scale * node_weight)
        node_colors.append(node_weight)
        
        # 构建节点标签
        label_parts = [f"Node {node}"]
        label_parts.append(f"Weight: {node_weight:.4f}")
        
        # 添加其他重要属性
        for attr_name, attr_value in G.nodes[node].items():
            if attr_name not in ['weight', 'center', 'index']:
                if isinstance(attr_value, (int, float)):
                    label_parts.append(f"{attr_name}: {attr_value:.4f}")
                else:
                    label_parts.append(f"{attr_name}: {attr_value}")
        
        node_labels.append(f"Node {node}")
        node_hover_texts.append("<br>".join(label_parts))
    
    # 3. 准备边数据
    edge_x = []
    edge_y = []
    edge_widths = []
    edge_colors = []
    edge_hover_texts = []
    
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        
        # 添加边的坐标（包括None用于分隔）
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        # 获取边属性
        edge_data = G[u][v]
        edge_weight = edge_data.get('weight', 1.0)
        edge_distance = edge_data.get('distance', 0.0)
        
        # 计算边宽度
        width = edge_size_scale * edge_weight
        edge_widths.extend([width, width, width])  # 为每个点重复
        
        # 边颜色
        edge_colors.extend(['rgba(128, 128, 128, 0.7)'] * 3)
        
        # 构建悬停文本
        hover_parts = [f"Edge ({u} ↔ {v})"]
        hover_parts.append(f"Weight: {edge_weight:.4f}")
        if 'distance' in edge_data:
            hover_parts.append(f"Distance: {edge_distance:.4f}")
        
        # 添加其他边属性
        for attr_name, attr_value in edge_data.items():
            if attr_name not in ['weight', 'distance']:
                if isinstance(attr_value, (int, float)):
                    hover_parts.append(f"{attr_name}: {attr_value:.4f}")
                else:
                    hover_parts.append(f"{attr_name}: {attr_value}")
        
        hover_text = "<br>".join(hover_parts)
        edge_hover_texts.extend([hover_text, hover_text, hover_text])
    
    # 4. 创建图形
    fig = go.Figure()
    
    # 添加边轨迹
    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode='lines',
        line=dict(
            width=edge_widths[0] if edge_widths else 1,
            color='rgba(128, 128, 128, 0.7)'
        ),
        hoverinfo='text',
        text=edge_hover_texts,
        name='Edges',
        showlegend=False
    ))
    
    # 添加节点轨迹
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers' + ('+text' if show_labels else ''),
        marker=dict(
            size=node_sizes,
            color=node_colors,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title="Node Weight",
                thickness=20,
                x=1.02
            ),
            line=dict(color='black', width=2)
        ),
        text=node_labels if show_labels else None,
        hovertext=node_hover_texts,
        hoverinfo='text',
        name='Nodes',
        textposition="top center",
        textfont=dict(size=12, color='black', family="Arial Black")
    ))
    
    # 5. 更新布局
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, family="Arial Black"),
            x=0.5
        ),
        showlegend=False,
        hovermode='closest',
        width=figsize[0],
        height=figsize[1],
        xaxis=dict(
            showgrid=True,
            zeroline=False,
            showticklabels=False,
            title='X Coordinate' if c is not None else None
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showticklabels=False,
            title='Y Coordinate' if c is not None else None
        ),
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # 6. 添加网络统计信息
    stats_text = f"""
    <b>Network Statistics:</b><br>
    • Nodes: {G.number_of_nodes()}<br>
    • Edges: {G.number_of_edges()}<br>
    • Average Node Weight: {np.mean(node_colors):.4f}<br>
    • Average Edge Weight: {np.mean([G[u][v].get('weight', 1.0) for u, v in G.edges()]) if G.number_of_edges() > 0 else 0:.4f}
    """
    
    fig.add_annotation(
        x=0.02,
        y=0.98,
        xref="paper",
        yref="paper",
        text=stats_text,
        showarrow=False,
        align="left",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
        bgcolor="white",
        opacity=0.9,
        font=dict(size=12)
    )
    
    return fig






    
from collections import defaultdict

def keep_top_k_edges_per_node(G, k, weight_attr='weight', inplace=False):
    """
    为每个节点保留权重最大的top k条边
    
    参数:
    G: NetworkX图
    k: 每个节点保留的最大边数
    weight_attr: 权重属性名
    inplace: 是否修改原图
    
    返回:
    处理后的图
    """
    if not inplace:
        H = G.copy()
    else:
        H = G
    
    # 如果k大于等于最大度，直接返回
    max_degree = max(dict(H.degree()).values(), default=0)
    if k >= max_degree:
        return H
    
    # 记录要删除的边
    edges_to_remove = set()
    
    for node in H.nodes():
        # 获取该节点的所有边及其权重
        edges = []
        for neighbor in H.neighbors(node):
            weight = H[node][neighbor].get(weight_attr, 1.0)
            edges.append((weight, node, neighbor))
        
        if len(edges) <= k:
            # 如果边数 <= k，保留所有边
            continue
        
        # 按权重排序，保留最大的k条边
        edges.sort(reverse=True, key=lambda x: x[0])
        edges_to_keep = set()
        
        for i in range(min(k, len(edges))):
            _, u, v = edges[i]
            # 确保每条边只被记录一次
            edge_key = (min(u, v), max(u, v)) if not H.is_directed() else (u, v)
            edges_to_keep.add(edge_key)
        
        # 标记要删除的边
        for _, u, v in edges:
            edge_key = (min(u, v), max(u, v)) if not H.is_directed() else (u, v)
            if edge_key not in edges_to_keep:
                edges_to_remove.add(edge_key)
    
    # 删除边
    if H.is_directed():
        edges_to_remove_list = [(u, v) for (u, v) in edges_to_remove]
    else:
        # 无向图需要确保双向都被删除
        edges_to_remove_list = list(edges_to_remove)
    
    H.remove_edges_from(edges_to_remove_list)
        
    return H