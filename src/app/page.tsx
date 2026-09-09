"use client";

import { useMemo, useState } from "react";

type Role = "Admin" | "Teacher" | "Student" | "Parent";

const roleCopy: Record<Role, { greeting: string; heading: string; subtitle: string; statLabels: string[]; values: string[] }> = {
  Admin: { greeting: "Good morning, Kiran", heading: "School at a glance", subtitle: "Everything across Academia is moving smoothly today.", statLabels: ["Students", "Teachers", "Attendance", "Fee collected"], values: ["1,284", "86", "94.2%", "$48,920"] },
  Teacher: { greeting: "Good morning, Priya", heading: "Your teaching day", subtitle: "You have three lessons and 24 submissions to review.", statLabels: ["Today’s lessons", "Submissions", "Class average", "Present today"], values: ["3", "24", "82%", "96%"] },
  Student: { greeting: "Good morning, Aanya", heading: "Ready for a great day?", subtitle: "You are on track - keep your 8-day learning streak going.", statLabels: ["Attendance", "Current average", "Assignments due", "Learning streak"], values: ["96%", "88%", "2", "8 days"] },
  Parent: { greeting: "Good morning, Meera", heading: "Aanya’s progress", subtitle: "A quick view of attendance, results, and what is coming up.", statLabels: ["Attendance", "Term average", "Due this week", "Outstanding fees"], values: ["96%", "88%", "2", "$0"] },
};

const navItems = [
  ["Overview", "home.png"], ["Students", "student.png"], ["Teachers", "teacher.png"], ["Classes", "class.png"],
  ["Attendance", "attendance.png"], ["Exams", "exam.png"], ["Finance", "finance.png"],
];

const schedule = [
  ["Mathematics", "08:30 - 09:20", "Room 204", "Indigo"],
  ["Physics", "09:35 - 10:25", "Science lab", "Sky"],
  ["English literature", "11:05 - 11:55", "Room 107", "Coral"],
];

export default function Home() {
  const [role, setRole] = useState<Role>("Admin");
  const [active, setActive] = useState("Overview");
  const [notice, setNotice] = useState("No new notifications");
  const copy = roleCopy[role];
  const activity = useMemo(() => role === "Teacher" ? ["24 submissions are ready for review", "Grade 8-A attendance was recorded", "Mathematics worksheet was published"] : ["Two new admission requests arrived", "Grade 8-A attendance was completed", "Term 2 results were published"], [role]);

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">A</span><span>Academia</span></div>
        <div className="school-switch"><span className="campus-dot" />Greenfield Academy <span className="chevron">⌄</span></div>
        <nav aria-label="Main navigation">
          {navItems.map(([label, icon]) => <button className={active === label ? "nav-item active" : "nav-item"} key={label} onClick={() => setActive(label)}><img src={`/${icon}`} alt="" />{label}</button>)}
        </nav>
        <div className="sidebar-bottom">
          <button className="nav-item"><img src="/setting.png" alt="" />Settings</button>
          <button className="profile-card" onClick={() => setNotice("Profile menu opened")}><img src="/avatar.png" alt="Kiran Chowdary" /><span><strong>Kiran Chowdary</strong><small>Administrator</small></span><b>⋮</b></button>
        </div>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <button className="mobile-brand" aria-label="Academia home">A</button>
          <div className="crumb"><span>Dashboard</span><b>/</b><strong>{active}</strong></div>
          <div className="top-actions">
            <label className="search"><img src="/search.png" alt="" /><input aria-label="Search" placeholder="Search anything..." /></label>
            <button className="icon-button" aria-label="Notifications" onClick={() => setNotice("You have 3 unread notifications")}><span className="notification-dot" />⌁</button>
            <select value={role} onChange={(event) => setRole(event.target.value as Role)} aria-label="View as role">
              {Object.keys(roleCopy).map((item) => <option key={item}>{item}</option>)}
            </select>
          </div>
        </header>

        <div className="content">
          <section className="hero">
            <div><p className="eyebrow">Wednesday, 14 August</p><h1>{copy.greeting}</h1><p>{copy.subtitle}</p></div>
            <button className="primary-button" onClick={() => setNotice("New record flow started")}>+ Add new</button>
          </section>

          <section className="stats" aria-label="School statistics">
            {copy.statLabels.map((label, index) => <article className="stat-card" key={label}><div className={`stat-icon icon-${index}`}><img src={`/${["student.png", "teacher.png", "singleAttendance.png", "finance.png"][index]}`} alt="" /></div><div><p>{label}</p><strong>{copy.values[index]}</strong><small className={index === 2 ? "positive" : "muted"}>{index === 2 ? "↑ 2.4% vs last week" : "Updated today"}</small></div></article>)}
          </section>

          <section className="dashboard-grid">
            <article className="panel attendance-panel"><div className="panel-title"><div><p className="eyebrow">This week</p><h2>Attendance overview</h2></div><button className="text-button">View report →</button></div><div className="chart"><div className="chart-y"><span>100</span><span>75</span><span>50</span><span>25</span><span>0</span></div><div className="bars">{[76, 88, 70, 94, 83, 58, 90].map((height, index) => <div className="bar-column" key={index}><i style={{ height: `${height}%` }} /><span>{["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][index]}</span></div>)}</div></div><div className="chart-foot"><span><i className="legend present" />Present 94.2%</span><span><i className="legend absent" />Absent 5.8%</span></div></article>
            <article className="panel activity-panel"><div className="panel-title"><div><p className="eyebrow">Updates</p><h2>Recent activity</h2></div><button className="text-button">See all →</button></div><ol>{activity.map((item, index) => <li key={item}><span className={`activity-dot dot-${index}`} /> <div><strong>{item}</strong><small>{index + 1} hour{index ? "s" : ""} ago</small></div></li>)}</ol></article>
          </section>

          <section className="lower-grid"><article className="panel schedule-panel"><div className="panel-title"><div><p className="eyebrow">Your agenda</p><h2>Today&apos;s schedule</h2></div><button className="text-button">Calendar →</button></div><div className="schedule-list">{schedule.map(([title, time, place, color]) => <div className="lesson" key={title}><span className={`lesson-mark ${color.toLowerCase()}`} /><div><strong>{title}</strong><small>{place}</small></div><time>{time}</time></div>)}</div></article><article className="panel quick-panel"><p className="eyebrow">Shortcuts</p><h2>Quick actions</h2><div className="quick-actions"><button onClick={() => setNotice("Attendance register opened")}><img src="/singleAttendance.png" alt="" />Mark attendance</button><button onClick={() => setNotice("New announcement composer opened")}><img src="/announcement.png" alt="" />Announcement</button><button onClick={() => setNotice("Report export started")}><img src="/result.png" alt="" />Export report</button><button onClick={() => setNotice("New student form opened")}><img src="/plus.png" alt="" />Add student</button></div></article></section>
        </div>
        <div className="toast" role="status">{notice}</div>
      </section>
    </main>
  );
}
