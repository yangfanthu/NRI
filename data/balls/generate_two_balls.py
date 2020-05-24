import numpy as np
import math
import matplotlib.pyplot as plt

import pdb
class TwoBalls():
	def __init__(self, time_resolution = 0.05, max_init_speed = 0.00001, min_init_x = 0, max_init_x = 3.0, max_init_y = 0.4,min_init_y = 0.25, max_distance = 0.25, output_steps = 15, max_w = 15, num_balls = 3):
		# the balls were constrained into y>0 plane
		self.time_resolution = time_resolution
		self.max_init_speed = max_init_speed
		self.min_init_x = min_init_x
		self.max_init_x = max_init_x
		self.max_init_y = max_init_y
		self.max_distance = max_distance
		self.min_resolution = 0.01
		self.output_steps = output_steps
		self.max_w = max_w
		self.num_balls = num_balls
		self.min_init_y = min_init_y
	def generate_data(self, num_data):
		total_time = self.output_steps * self.time_resolution
		total_ball_trajs = []
		num_balls = []
		for i in range(num_data):	
			center_x = np.random.uniform(self.min_init_x, self.max_init_x)
			center_y = np.random.uniform(self.min_init_y, self.max_init_y)  # min init y is default to be 0
			orn = np.random.uniform(0, math.pi)
			distance = np.random.uniform(0, self.max_distance)
			vx = np.random.uniform(-self.max_init_speed, self.max_init_speed)
			vy = np.random.uniform(-self.max_init_speed, self.max_init_speed)
			w = np.random.uniform(-self.max_w, self.max_w)
			# w = 10
			connect_flag = True
			balls = self.get_ball_pos(center_x, center_y, orn, distance)
			ball_v = self.get_ball_v(vx, vy, orn, w, distance)
			# balls = np.zeros((self.num_balls,2))
			# balls_v = np.zeros((self.num_balls,2))
			ball_trajs = []
			for t_index in range(int(total_time / self.min_resolution)):
				if connect_flag:
					orn = orn + w * self.min_resolution
					center_x = center_x + vx * self.min_resolution
					center_y = center_y + vy * self.min_resolution
					balls = self.get_ball_pos(center_x, center_y, orn, distance)
					ball_v = self.get_ball_v(vx, vy, orn, w, distance)
					for i in range(self.num_balls):
						if balls[i,1] < 0:
							connect_flag = False
							# if ball_v[i,1] < 0:
							# 	ball_v[i,1] = -ball_v[i,1]
				else:
					# print("broken", t_index)
					for i in range(self.num_balls):
						if balls[i,1] < 0:
							connect_flag = False
							# if ball_v[i,1] < 0:
							# 	ball_v[i,1] = -ball_v[i,1]
					balls = balls + ball_v * self.min_resolution
					
				ball_trajs.append(balls)
			ball_trajs = np.stack(ball_trajs, axis = 1)
			final_ball_trajs = np.zeros((self.num_balls, self.output_steps, 2))
			for t_index in range(self.output_steps):
				final_ball_trajs[:,t_index] = ball_trajs[:,int(t_index * self.time_resolution / self.min_resolution)]

			# self.plot_traj(final_ball_trajs)
			# pdb.set_trace()
			total_ball_trajs.append(final_ball_trajs)
			#total_ball_trajs shape [case, ball, time, dimension]
			num_balls.append(self.num_balls)
		total_ball_trajs = np.array(total_ball_trajs)
		num_balls = np.array(num_balls)
		np.save("./balls.npy", total_ball_trajs)




	def get_ball_pos(self, center_x, center_y, orn, distance):
		balls = np.zeros((self.num_balls, 2))
		for i in range(self.num_balls):
			x = center_x + distance * math.cos(orn + i * 2 * math.pi / self.num_balls)
			y = center_y + distance * math.sin(orn + i * 2 * math.pi / self.num_balls)
			balls[i,0] = x
			balls[i,1] = y
		return balls
	def get_ball_v(self, center_vx, center_vy, orn, w, distance):
		ball_v = np.zeros((self.num_balls, 2))
		for i in range(self.num_balls):
			vx = center_vx + distance * w * math.cos(orn + math.pi / 2 + i * 2 * math.pi / self.num_balls)
			vy = center_vy + distance * w * math.sin(orn + math.pi / 2 + i * 2 * math.pi / self.num_balls)
			ball_v[i,0] = vx
			ball_v[i,1] = vy
		return ball_v
	def plot_traj(self, ball_trajs):
		color_table = [u'#1f77b4', u'#ff7f0e', u'#2ca02c', u'#d62728', u'#9467bd', u'#8c564b', u'#e377c2', u'#7f7f7f', u'#bcbd22', u'#17becf','floralwhite']
		for i in range(self.output_steps):
			for ball_index in range(self.num_balls):
				plt.scatter(ball_trajs[ball_index,i,0], ball_trajs[ball_index,i,1], c = color_table[ball_index],alpha = 0.3 + i * 0.7 / self.output_steps)
		for i in range(self.output_steps):
			for ball_index in range(self.num_balls - 1):
				plt.plot([ball_trajs[ball_index,i, 0], ball_trajs[ball_index+1,i,0]], [ball_trajs[ball_index,i, 1], ball_trajs[ball_index + 1,i,1]], c = "g" , alpha = 0.3 + i * 0.7 / self.output_steps)
		plt.show()





if __name__ == "__main__":
	generator = TwoBalls()
	generator.generate_data(num_data = 10000)
