import StatsCards from '../components/StatsCards';
import QuotaBar from '../components/QuotaBar';
import AddHRForm from '../components/AddHRForm';
import LeadsTable from '../components/LeadsTable';

export default function Dashboard() {
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div>
          <h1 className="main-title">Cold Outreach Hub</h1>
          <p className="main-subtitle">Automate your HR outreach with GenAI 🚀</p>
        </div>
        <div className="header-actions">
          <QuotaBar />
        </div>
      </header>

      <main className="dashboard-main">
        {/* Top Stats */}
        <section className="dashboard-section section-stats">
          <StatsCards />
        </section>

        <div className="dashboard-grid">
          {/* Left Column: Form */}
          <aside className="dashboard-sidebar">
            <AddHRForm />
          </aside>

          {/* Right Column: Table */}
          <section className="dashboard-content">
            <LeadsTable />
          </section>
        </div>
      </main>
    </div>
  );
}
