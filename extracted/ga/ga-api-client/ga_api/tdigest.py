import math
# To use in pandas df['PR90'] = df['tDigest'].apply(lambda x: x.quantile(0.9))
# print tDigest would output the median
# Supported Method: min, max, mean, sum, empty, quantile

class Centroid:
    def __init__(self, mean, weight):
        self.mean = mean
        self.weight = weight

    def update(self, sum_, weight):
        sum_ += self.mean * self.weight
        self.weight += weight
        self.mean = sum_ / self.weight
        return sum_

class TDigest:
    def __init__(self, arg=[[math.inf, 0, 64]]):
        centroids = arg[1:]
        self.centroids = []
        self.min = arg[0][0]
        self.max = arg[0][1]
        self.count = 0
        self.sum = 0
        self.max_size = arg[0][2]

        for c in centroids:
            # Assume each centroid is a tuple (mean, weight)
            self.sum += c[0] * c[1]
            self.count += c[1]
            self.centroids.append(Centroid(c[0], c[1]))
    
    def __add__(self, other):
        new_one = TDigest([[math.inf, 0, max(self.max_size, other.max_size)]])
        new_one.update(self)
        new_one.update(other)
        return new_one
    
    def __radd__(self, other):
        new_one = TDigest([[math.inf, 0, max(self.max_size, other.max_size)]])
        new_one.update(self)
        new_one.update(other)
        return new_one
    
    def __iadd__(self, other):
        self.update(other)
        return self
    
    def __str__(self):
        return f'{self.quantile(0.5)}'
    
    def __repr__(self):
        return f'$tDigest({self.output()})'
    
    def output(self):
        centroids = [[c.mean, c.weight] for c in self.centroids]
        centroids.insert(0, [self.min, self.max, self.max_size])
        return centroids

    def __k_to_q(self, k, d):
        k_div_d = k / d
        if k_div_d >= 0.5:
            base = 1 - k_div_d
            return 1 - 2 * base * base
        else:
            return 2 * k_div_d * k_div_d

    def update(self, another):
        if not isinstance(another, TDigest):
            return

        new_centroids = []
        self.centroids.extend(another.centroids)
        self.centroids.sort(key=lambda c: c.mean)
        self.min = min(self.min, another.min)
        self.max = max(self.max, another.max)
        self.count += another.count

        new_sum = 0
        k_limit = 1
        q_limit_times_count = self.__k_to_q(k_limit, self.max_size) * self.count
        k_limit += 1

        centroid_idx = 0
        cur_centroid = self.centroids[centroid_idx]
        centroid_idx += 1

        weight_so_far = cur_centroid.weight
        sums_to_merge = 0
        weight_to_merge = 0

        for _ in range(1, len(self.centroids)):
            next_centroid = self.centroids[centroid_idx]
            centroid_idx += 1

            next_sum = next_centroid.mean * next_centroid.weight
            weight_so_far += next_centroid.weight

            if weight_so_far <= q_limit_times_count:
                sums_to_merge += next_sum
                weight_to_merge += next_centroid.weight
            else:
                new_sum += cur_centroid.update(sums_to_merge, weight_to_merge)
                sums_to_merge = 0
                weight_to_merge = 0
                new_centroids.append(cur_centroid)

                q_limit_times_count = self.__k_to_q(k_limit, self.max_size) * self.count
                k_limit += 1
                cur_centroid = next_centroid

        new_sum += cur_centroid.update(sums_to_merge, weight_to_merge)
        new_centroids.append(cur_centroid)

        self.centroids = new_centroids
        self.sum = new_sum

    def quantile(self, q):
        if q <= 0:
            return self.min
        elif q >= 1:
            return self.max
        elif self.count == 0:
            return math.nan

        rank = q * self.count
        pos = None
        weight_so_far = None

        if q > 0.5:
            pos = 0
            weight_so_far = self.count
            for i in range(len(self.centroids) - 1, -1, -1):
                weight_so_far -= self.centroids[i].weight
                if rank >= weight_so_far:
                    pos = i
                    break
        else:
            pos = len(self.centroids) - 1
            weight_so_far = 0
            for i, centroid in enumerate(self.centroids):
                if rank < weight_so_far + centroid.weight:
                    pos = i
                    break
                weight_so_far += centroid.weight

        delta = 0
        min_ = self.min
        max_ = self.max

        if len(self.centroids) > 1:
            if pos == 0:
                delta = self.centroids[pos + 1].mean - self.centroids[pos].mean
                max_ = self.centroids[pos + 1].mean
            elif pos == len(self.centroids) - 1:
                delta = self.centroids[pos].mean - self.centroids[pos - 1].mean
                min_ = self.centroids[pos - 1].mean
            else:
                delta = (self.centroids[pos + 1].mean - self.centroids[pos - 1].mean) / 2
                min_ = self.centroids[pos - 1].mean
                max_ = self.centroids[pos + 1].mean

        value = (self.centroids[pos].mean +
                 ((rank - weight_so_far) / self.centroids[pos].weight - 0.5) * delta)

        if value < min_:
            value = min_
        elif value > max_:
            value = max_

        return value

    def mean(self):
        return self.sum / self.count if self.count > 0 else math.nan

    def sum(self):
        return self.sum

    def min(self):
        return self.min

    def max(self):
        return self.max

    def empty(self):
        return self.count == 0

    def max_size(self):
        return self.max_size
