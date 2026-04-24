import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getLeads, addLead, deleteLead, updateLeadStatus, checkDuplicate } from '../api/client';
import toast from 'react-hot-toast';

export const useLeads = (filters = {}) =>
  useQuery({
    queryKey: ['leads', filters],
    queryFn: () => getLeads(filters),
    refetchInterval: 10000,
  });

export const useAddLead = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: addLead,
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ['leads'] });
      qc.invalidateQueries({ queryKey: ['stats'] });
      qc.invalidateQueries({ queryKey: ['quota'] });
      if (data.status === 'sent') toast.success(`✅ Email sent to ${data.hr_name}!`);
      else if (data.status === 'queued') toast(`📋 Quota full — queued for ${data.hr_name}`, { icon: '🔵' });
      else toast.error(`❌ Failed for ${data.hr_name}`);
    },
    onError: (err) => {
      const msg = err?.response?.data?.detail || err.message;
      toast.error(msg);
    },
  });
};

export const useDeleteLead = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: deleteLead,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['leads'] });
      qc.invalidateQueries({ queryKey: ['stats'] });
      toast.success('Lead deleted');
    },
  });
};

export const useUpdateStatus = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, status }) => updateLeadStatus(id, status),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['leads'] });
      toast.success('Status updated');
    },
  });
};

export const useCheckDuplicate = () =>
  useMutation({ mutationFn: checkDuplicate });
