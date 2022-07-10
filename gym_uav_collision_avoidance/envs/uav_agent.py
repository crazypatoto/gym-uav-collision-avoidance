import gym
import pygame
import numpy as np

class UAVAgent():
    def __init__(self, color, max_speed=10, max_acceleraion=4, d_sense=30, tau=0.02):
        self.color = color
        self.max_speed = np.array([max_speed, max_speed])
        self.max_acceleration = np.array([max_acceleraion, max_acceleraion])
        self.d_sense = d_sense
        self.tau = tau        
        self.location = np.zeros(2)
        self.velocity = np.zeros(2)
        self.velocity_prev = np.zeros(2)        
        self.target_location = np.zeros(2)
        self.init_distance = 0
        self.prev_distance = 0
    
    
    def step(self, action):
        dv = np.clip((action - self.velocity_prev)/self.tau, -self.max_acceleration, self.max_acceleration)
        self.velocity = np.clip(self.velocity_prev + dv * self.tau, -self.max_speed, self.max_speed)
        dx = self.velocity * self.tau        
        self.location += dx
        self.velocity_prev = self.velocity
    
    def uavs_in_range(self, uav_agents):
        uavs = []
        relative_distances = []
        for i in range(len(uav_agents)):
            target_agent = uav_agents[i]
            if target_agent == self:
                continue
            distance = np.linalg.norm(target_agent.location - self.location)
            if np.linalg.norm(target_agent.location - self.location) < self.d_sense:
                uavs.append(target_agent)
                relative_distances.append(distance)
        
        # Sort UAVs with relative distances 
        return [x for _,x in sorted(zip(relative_distances,uavs))] if len(uavs) > 0 else []
        
       