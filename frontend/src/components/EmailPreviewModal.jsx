import { X, Mail, Globe, Link as Linkedin, Calendar, Clock, AlertTriangle } from 'lucide-react';

const STATUS_MAP = {
  pending:  { label: 'Pending',  cls: 'badge-pending'  },
  queued:   { label: 'Queued',   cls: 'badge-queued'   },
  sent:     { label: 'Sent',     cls: 'badge-sent'      },
  failed:   { label: 'Failed',   cls: 'badge-failed'   },
  replied:  { label: 'Replied',  cls: 'badge-replied'  },
};

export default function EmailPreviewModal({ lead, onClose, onStatusChange }) {
  if (!lead) return null;
  const { label, cls } = STATUS_MAP[lead.status] || { label: lead.status, cls: '' };

  const fmt = (ts) =>
    ts ? new Date(ts).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' }) : '—';

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <h2 className="modal-title">{lead.hr_name}</h2>
            <p className="modal-sub">
              {lead.hr_position && <span>{lead.hr_position} @ </span>}
              <strong>{lead.company}</strong>
            </p>
          </div>
          <button className="btn-close" onClick={onClose}><X size={20} /></button>
        </div>

        <div className="modal-meta">
          <a href={`mailto:${lead.hr_email}`} className="meta-chip">
            <Mail size={14} /> {lead.hr_email}
          </a>
          {lead.company_url && (
            <a href={lead.company_url} target="_blank" rel="noreferrer" className="meta-chip">
              <Globe size={14} /> Website
            </a>
          )}
          {lead.linkedin_url && (
            <a href={lead.linkedin_url} target="_blank" rel="noreferrer" className="meta-chip">
              <Linkedin size={14} /> LinkedIn
            </a>
          )}
          <span className={`badge ${cls}`}>{label}</span>
        </div>

        <div className="modal-timestamps">
          <span><Calendar size={13}/> Added: {fmt(lead.created_at)}</span>
          {lead.sent_at   && <span><Clock size={13}/> Sent: {fmt(lead.sent_at)}</span>}
          {lead.queued_at && <span><Clock size={13}/> Queued: {fmt(lead.queued_at)}</span>}
        </div>

        {lead.notes && (
          <div className="modal-section">
            <h3 className="section-label">Notes</h3>
            <p className="notes-text">{lead.notes}</p>
          </div>
        )}

        {lead.email_subject ? (
          <div className="modal-section">
            <h3 className="section-label">Generated Email</h3>
            <div className="email-preview">
              <div className="email-subject">Subject: {lead.email_subject}</div>
              <pre className="email-body">{lead.email_body}</pre>
            </div>
          </div>
        ) : (
          <div className="modal-section empty-email">
            <AlertTriangle size={16} /> No email generated yet.
          </div>
        )}

        {lead.error_log && (
          <div className="modal-section error-box">
            <h3 className="section-label">Error Log</h3>
            <pre className="error-text">{lead.error_log}</pre>
          </div>
        )}

        <div className="modal-footer">
          <span className="footer-label">Update Status:</span>
          {['pending', 'queued', 'sent', 'failed', 'replied'].map((s) => (
            <button
              key={s}
              className={`btn btn-sm ${lead.status === s ? 'btn-active' : 'btn-ghost'}`}
              onClick={() => onStatusChange(lead.id, s)}
            >
              {s}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
