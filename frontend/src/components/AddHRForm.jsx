import { useState } from 'react';
import { useAddLead, useCheckDuplicate } from '../hooks/useLeads';
import { Briefcase, Building, Mail, User, Link as LinkIcon, Globe, FileText, Send, Loader2 } from 'lucide-react';
import { useQueryClient } from '@tanstack/react-query';

export default function AddHRForm() {
  const [formData, setFormData] = useState({
    hr_name: '', hr_email: '', hr_position: '', company: '', 
    company_url: '', linkedin_url: '', notes: ''
  });
  const [duplicateWarning, setDuplicateWarning] = useState(null);
  
  const { mutate: addLead, isPending: isAdding } = useAddLead();
  const { mutateAsync: checkDuplicate } = useCheckDuplicate();
  const queryClient = useQueryClient();

  const handleChange = (e) => setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));

  const handleEmailBlur = async () => {
    if (!formData.hr_email || !formData.hr_email.includes('@')) return;
    try {
      const res = await checkDuplicate(formData.hr_email);
      if (res.is_duplicate) {
        setDuplicateWarning(`Already ${res.status} on ${res.sent_at || res.created_at}`);
      } else {
        setDuplicateWarning(null);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (duplicateWarning) {
      const proceed = window.confirm("This email is already in the system. Are you sure you want to add it again?");
      if (!proceed) return;
    }
    
    addLead(formData, {
      onSuccess: () => {
        setFormData({ hr_name: '', hr_email: '', hr_position: '', company: '', company_url: '', linkedin_url: '', notes: '' });
        setDuplicateWarning(null);
        queryClient.invalidateQueries({ queryKey: ['leads'] });
        queryClient.invalidateQueries({ queryKey: ['stats'] });
        queryClient.invalidateQueries({ queryKey: ['quota'] });
      }
    });
  };

  return (
    <div className="form-card">
      <h2 className="form-title">⚡ Add New HR Lead</h2>
      <p className="form-subtitle">Enter details to auto-generate and send a custom cold email.</p>
      
      {duplicateWarning && (
        <div className="alert-duplicate">
          ⚠️ <strong>Duplicate found:</strong> {duplicateWarning}
        </div>
      )}

      <form onSubmit={handleSubmit} className="hr-form">
        <div className="form-row">
          <div className="form-group">
            <label><User size={14}/> HR Name*</label>
            <input required name="hr_name" value={formData.hr_name} onChange={handleChange} className="input" placeholder="e.g. Sarah Connor" />
          </div>
          <div className="form-group">
            <label><Mail size={14}/> HR Email*</label>
            <input required type="email" name="hr_email" value={formData.hr_email} onChange={handleChange} onBlur={handleEmailBlur} className="input" placeholder="sarah@company.com" />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label><Briefcase size={14}/> Position</label>
            <input name="hr_position" value={formData.hr_position} onChange={handleChange} className="input" placeholder="e.g. Technical Recruiter" />
          </div>
          <div className="form-group">
            <label><Building size={14}/> Company*</label>
            <input required name="company" value={formData.company} onChange={handleChange} className="input" placeholder="Company Name" />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label><Globe size={14}/> Company URL</label>
            <input type="url" name="company_url" value={formData.company_url} onChange={handleChange} className="input" placeholder="https://..." />
          </div>
          <div className="form-group">
            <label><LinkIcon size={14}/> LinkedIn URL</label>
            <input type="url" name="linkedin_url" value={formData.linkedin_url} onChange={handleChange} className="input" placeholder="https://linkedin.com/in/..." />
          </div>
        </div>

        <div className="form-group">
          <label><FileText size={14}/> Extra Notes / Context</label>
          <textarea 
            name="notes" 
            value={formData.notes} 
            onChange={handleChange} 
            className="input textarea" 
            placeholder="Mention any specific context... e.g., 'They recently raised Series B' or 'Hiring for Frontend Engineers'"
            rows={3}
          />
        </div>

        <button type="submit" className="btn btn-primary w-full" disabled={isAdding}>
          {isAdding ? <><Loader2 size={16} className="spin" /> Processing AI Email...</> : <><Send size={16} /> Generate & Send Email</>}
        </button>
      </form>
    </div>
  );
}
