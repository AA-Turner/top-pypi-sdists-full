import numpy as np


class PathOptimizerMixin:
    def get_radius(self, pos):
        return np.sqrt(np.abs(pos[:, 0]) ** 2 + np.abs(pos[:, 1]) ** 2)

    def optimize_corridor(self, positions, corridor_size=None, sort_axis=1, num_iterations=1):
        if len(positions[0]) < 2:
            return positions
        if corridor_size is None:
            dims = [
                abs(min(positions[:, 0]) - max(positions[:, 0])),
                abs(min(positions[:, 1]) - max(positions[:, 1])),
            ]
            density = np.sqrt(len(positions) / (dims[1] * dims[0]))
            corridor_size = 2 / density

        result = [np.inf, []]
        if num_iterations > 1:
            corridor_sizes = np.linspace(corridor_size / 2, corridor_size * 2, num_iterations)
        else:
            corridor_sizes = [corridor_size]
        for corridor_size_iter in corridor_sizes:
            index_sorted = []

            n_steps = int(
                np.round(
                    np.abs(max(positions[:, sort_axis]) - min(positions[:, sort_axis]))
                    / corridor_size_iter
                )
            )
            steps = list(
                np.floor(
                    np.linspace(min(positions[:, sort_axis]), max(positions[:, sort_axis]), n_steps)
                )
            )
            # print(steps, n_steps, positions)
            steps.append(np.inf)
            for step in range(n_steps):
                block = np.where(positions[:, sort_axis] >= steps[step])
                block = block[0][np.where(positions[:, sort_axis][block[0]] < steps[step + 1])]
                block = block[np.argsort(positions[:, int(not sort_axis)][block])]
                if step % 2 == 0:
                    block = block[::-1]
                index_sorted.append(block)
            path_length = self.get_path_length(positions[np.concatenate(index_sorted), :])
            if path_length < result[0]:
                result = [path_length, positions[np.concatenate(index_sorted), :]]
        return result[1]

    def optimize_shell(self, pos, offset, dr):
        max_rad_id = np.where(self.get_radius(pos) == np.max(self.get_radius(pos)))
        max_rad = self.get_radius(pos[max_rad_id])[0]

        sub_groups = []
        nsteps = int(np.floor(max_rad / dr) + int(bool(np.mod(max_rad, dr))))
        sub_rad_prev = -offset * dr
        for i in range(nsteps + 2):
            temp = np.where(self.get_radius(pos) < dr + sub_rad_prev)
            temp = temp[0][np.where(self.get_radius(pos[temp[0]]) >= sub_rad_prev)]
            temp_pos = pos[temp]
            angles = np.arctan2(temp_pos[:, 0], (temp_pos[:, 1]))
            pos_sort = temp_pos[np.argsort(angles)]
            sub_groups.append(pos_sort)
            sub_rad_prev += dr

        temp = np.where(self.get_radius(pos) >= sub_rad_prev)
        temp = temp[0][np.where(self.get_radius(pos[temp[0]]) >= sub_rad_prev)]
        temp_pos = pos[temp]
        angles = np.arctan2(temp_pos[:, 0], (temp_pos[:, 1]))
        pos_sort = temp_pos[np.argsort(angles)]
        sub_groups.append(pos_sort)

        posi = []
        for i in range(len(sub_groups)):
            for j in range(len(sub_groups[i])):
                posi.extend([sub_groups[i][j]])

        return np.asarray(posi)

    def get_path_length(self, pos):
        path_length = 0
        for ii in range(len(pos) - 1):
            path_length += np.sqrt(np.sum(abs(pos[ii + 1] - pos[ii]) ** 2))
        return path_length
