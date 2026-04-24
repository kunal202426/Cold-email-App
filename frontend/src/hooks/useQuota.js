import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getQuota, getStats, processQueue } from '../api/client';
import toast from 'react-hot-toast';

export const useQuota = () =>
  useQuery({
    queryKey: ['quota'],
    queryFn: getQuota,
    refetchInterval: 15000,
  });

export const useStats = () =>
  useQuery({
    queryKey: ['stats'],
    queryFn: getStats,
    refetchInterval: 15000,
  });

export const useProcessQueue = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: processQueue,
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ['leads'] });
      qc.invalidateQueries({ queryKey: ['quota'] });
      qc.invalidateQueries({ queryKey: ['stats'] });
      toast.success(`Queue processed: ${data.sent} sent, ${data.failed} failed`);
    },
    onError: (err) => {
      const msg = err?.response?.data?.detail || err.message;
      toast.error(msg);
    },
  });
};
