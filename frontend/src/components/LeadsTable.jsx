import { useState } from 'react';
import { useLeads, useDeleteLead, useUpdateStatus } from '../hooks/useLeads';
import EmailPreviewModal from './EmailPreviewModal';
import { Trash2, Eye, RefreshCcw } from 'lucide-react';

const STATUS_MAP = {
  pending:  { label: '🟡 Pending',  cls: 'badge-pending'  },
  queued:   { label: '🔵 Queued',   cls: 'badge-queued'   },
  sent:     { label: '🟢 Sent',     cls: 'badge-sent'      },
  failed:   { label: '🔴 Failed',   cls: 'badge-failed'   },
  replied:  { label: '💬 Replied',  cls: 'badge-replied'  },
};

const STATUSES = ['all', 'pending', 'queued', 'sent', 'failed', 'replied'];

export default function LeadsTable() {
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterCompany, setFilterCompany] = useState('');
  const [selectedLead, setSelectedLead] = useState(null);

  const filters = {};
  if (filterStatus !== 'all') filters.status = filterStatus;
  if (filterCompany.trim()) filters.company = filterCompany.trim();

  const { data: leads = [], isLoading, refetch } = useLeads(filters);
  const { mutate: deleteLead } = useDeleteLead();
  const { mutate: updateStatus } = useUpdateStatus();

  const handleStatusChange = (id, status) => {
    updateStatus({ id, status });
    setSelectedLead((prev) => prev ? { ...prev, status } : prev);
  };

  const fmt = (ts) =>
    ts ? new Date(ts).toLocaleString('en-IN', { dateStyle: 'short', timeStyle: 'short' }) : '—';

  return (
    <div className="leads-section">
      {/* Filters */}
      <div className="leads-filters">
        <div className="filter-group">
          {STATUSES.map((s) => (
            <button
              key={s}
              className={`filter-chip ${filterStatus === s ? 'active' : ''}`}
              onClick={() => setFilterStatus(s)}
            >
              {s === 'all' ? 'All' : STATUS_MAP[s]?.label || s}
            </button>
          ))}
        </div>
        <div className="search-wrap">
          <input
            className="input search-input"
            placeholder="Filter by company…"
            value={filterCompany}
            onChange={(e) => setFilterCompany(e.target.value)}
          />
          <button className="btn btn-ghost btn-sm" onClick={() => refetch()} title="Refresh">
            <RefreshCcw size={14} />
          </button>
        </div>
      </div>

      {/* Table */}
      {isLoading ? (
        <div className="table-empty">Loading…</div>
      ) : leads.length === 0 ? (
        <div className="table-empty">No leads found. Add your first HR! 🚀</div>
      ) : (
        <div className="table-wrap">
          <table className="leads-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Company</th>
                <th>Position</th>
                <th>Status</th>
                <th>Sent At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {leads.map((lead) => {
                const { label, cls } = STATUS_MAP[lead.status] || { label: lead.status, cls: '' };
                return (
                  <tr key={lead.id} className="lead-row" onClick={() => setSelectedLead(lead)}>
                    <td>
                      <div className="lead-name">{lead.hr_name}</div>
                      <div className="lead-email">{lead.hr_email}</div>
                    </td>
                    <td>{lead.company}</td>
                    <td>{lead.hr_position || '—'}</td>
                    <td><span className={`badge ${cls}`}>{label}</span></td>
                    <td className="ts">{fmt(lead.sent_at || lead.queued_at || lead.created_at)}</td>
                    <td onClick={(e) => e.stopPropagation()}>
                      <div className="action-btns">
                        <button
                          className="btn btn-icon"
                          title="Preview email"
                          onClick={() => setSelectedLead(lead)}
                        >
                          <Eye size={15} />
                        </button>
                        <button
                          className="btn btn-icon btn-danger"
                          title="Delete lead"
                          onClick={() => {
                            if (confirm(`Delete ${lead.hr_name}?`)) deleteLead(lead.id);
                          }}
                        >
                          <Trash2 size={15} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {selectedLead && (
        <EmailPreviewModal
          lead={selectedLead}
          onClose={() => setSelectedLead(null)}
          onStatusChange={handleStatusChange}
        />
      )}
    </div>
  );
}
