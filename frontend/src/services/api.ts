import axios, { AxiosError } from 'axios';
import type { User, Project, Task, AuthResponse, ApiError } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const handleApiError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>;
    if (axiosError.response?.data?.error) {
      const { error: message, fields } = axiosError.response.data;
      if (fields) {
        const fieldErrors = Object.entries(fields)
          .map(([key, value]) => `${key} ${value}`)
          .join(', ');
        return `${message}: ${fieldErrors}`;
      }
      return message;
    }
    return axiosError.message;
  }
  return 'An unexpected error occurred';
};

export const authApi = {
  register: async (name: string, email: string, password: string): Promise<AuthResponse> => {
    const { data } = await api.post<AuthResponse>('/auth/register', { name, email, password });
    return data;
  },

  login: async (email: string, password: string): Promise<AuthResponse> => {
    const { data } = await api.post<AuthResponse>('/auth/login', { email, password });
    return data;
  },
};

export const projectsApi = {
  list: async (page: number = 1, limit: number = 20): Promise<{ projects: Project[]; pagination: any }> => {
    const { data } = await api.get<{ projects: Project[]; pagination: any }>('/projects', {
      params: { page, limit }
    });
    return data;
  },

  create: async (name: string, description?: string): Promise<Project> => {
    const { data } = await api.post<Project>('/projects', { name, description });
    return data;
  },

  get: async (id: string): Promise<Project> => {
    const { data } = await api.get<Project>(`/projects/${id}`);
    return data;
  },

  update: async (id: string, updates: Partial<Pick<Project, 'name' | 'description'>>): Promise<Project> => {
    const { data } = await api.patch<Project>(`/projects/${id}`, updates);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/projects/${id}`);
  },
};

export const tasksApi = {
  list: async (
    projectId: string, 
    filters?: { status?: string; assignee?: string; page?: number; limit?: number }
  ): Promise<{ tasks: Task[]; pagination: any }> => {
    const { data } = await api.get<{ tasks: Task[]; pagination: any }>(`/projects/${projectId}/tasks`, { 
      params: filters 
    });
    return data;
  },

  create: async (projectId: string, task: Partial<Task>): Promise<Task> => {
    const { data } = await api.post<Task>(`/projects/${projectId}/tasks`, task);
    return data;
  },

  update: async (id: string, updates: Partial<Task>): Promise<Task> => {
    const { data } = await api.patch<Task>(`/tasks/${id}`, updates);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/tasks/${id}`);
  },
};

export default api;
