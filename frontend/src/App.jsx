import { useMemo, useState } from "react";

const books = [
  { title: "The Silent Patient", author: "Alex Michaelides", genre: "Thriller", cover: "https://covers.openlibrary.org/b/isbn/9781250301697-L.jpg", progress: 72, color: "#9a493f" },
  { title: "Tomorrow, and Tomorrow, and Tomorrow", author: "Gabrielle Zevin", genre: "Fiction", cover: "https://covers.openlibrary.org/b/isbn/9780593321201-L.jpg", progress: 0, color: "#d77c20" },
  { title: "The Midnight Library", author: "Matt Haig", genre: "Fantasy", cover: "https://covers.openlibrary.org/b/isbn/9780525559474-L.jpg", progress: 100, color: "#245b83" },
  { title: "Educated", author: "Tara Westover", genre: "Memoir", cover: "https://covers.openlibrary.org/b/isbn/9780399590504-L.jpg", progress: 38, color: "#80715d" },
  { title: "The House in the Cerulean Sea", author: "TJ Klune", genre: "Fantasy", cover: "https://covers.openlibrary.org/b/isbn/9781250217288-L.jpg", progress: 0, color: "#258a91" },
  { title: "Project Hail Mary", author: "Andy Weir", genre: "Science Fiction", cover: "https://covers.openlibrary.org/b/isbn/9780593135204-L.jpg", progress: 100, color: "#aa682d" },
  { title: "A Little Life", author: "Hanya Yanagihara", genre: "Fiction", cover: "https://covers.openlibrary.org/b/isbn/9780804172707-L.jpg", progress: 0, color: "#72809a" },
  { title: "The Song of Achilles", author: "Madeline Miller", genre: "Fantasy", cover: "https://covers.openlibrary.org/b/isbn/9780062060624-L.jpg", progress: 0, color: "#8f423f" },
  { title: "Atomic Habits", author: "James Clear", genre: "Personal Growth", cover: "https://covers.openlibrary.org/b/isbn/9780735211292-L.jpg", progress: 54, color: "#477e69" },
  { title: "The Seven Husbands of Evelyn Hugo", author: "Taylor Jenkins Reid", genre: "Fiction", cover: "https://covers.openlibrary.org/b/isbn/9781501161933-L.jpg", progress: 100, color: "#b94755" },
];

const navGroups = [
  { title: "Workspace", items: [["▦", "Dashboard"], ["♙", "Authors"], ["▤", "Series"], ["⌕", "Tools"]] },
  { title: "Libraries", items: [["◖", "Audiobooks", "26"], ["▣", "Books", "195"], ["◇", "Comics", "23"], ["▤", "PDFs", "9"]] },
  { title: "Smart scopes", items: [["♧", "Ancient Wisdom", "1"], ["⬡", "Format Hoarders", "11"], ["⌕", "ISBN Mysteries", "82"], ["◉", "Metadata Ghosts", "162"], ["✳", "Polyglot Shelf", "60"]] },
  { title: "Collections", items: [["♧", "Backlog", "19"], ["▣", "Hardcover", "7"]] },
];

function BookCover({ book, compact = false }) {
  return <div className={`book-cover ${compact ? "compact" : ""}`} style={{ "--cover-color": book.color }}>
    <img src={book.cover} alt={`${book.title} cover`} onError={(e) => { e.currentTarget.style.display = "none"; }} />
    <span className="cover-fallback"><small>{book.author}</small><strong>{book.title}</strong></span>
  </div>;
}

function Shelf({ title, icon, items, onSelect }) {
  return <section className="shelf panel">
    <div className="section-heading"><h2><span>{icon}</span>{title}</h2><button className="text-button">View all <span>↗</span></button></div>
    <div className="book-row">{items.map((book) => <button className="book-tile" key={book.title} onClick={() => onSelect(book)}>
      <BookCover book={book} /><span className="book-title">{book.title}</span><span className="book-author">{book.author}</span>
    </button>)}</div>
  </section>;
}

export default function App() {
  const [query, setQuery] = useState("");
  const [activeNav, setActiveNav] = useState("Dashboard");
  const [selected, setSelected] = useState(null);
  const [goal, setGoal] = useState(12);
  const [menuOpen, setMenuOpen] = useState(false);
  const visibleBooks = useMemo(() => books.filter((book) => `${book.title} ${book.author}`.toLowerCase().includes(query.toLowerCase())), [query]);
  const reading = books.filter((book) => book.progress > 0 && book.progress < 100);
  const completed = books.filter((book) => book.progress === 100);

  return <main className="app-shell">
    <aside className={`sidebar ${menuOpen ? "open" : ""}`}>
      <button className="brand" onClick={() => setActiveNav("Dashboard")}><span className="brand-mark">◉</span><span><b>Book Orbit</b><small>YOUR READING SPACE</small></span><span className="sidebar-toggle" onClick={(e) => { e.stopPropagation(); setMenuOpen(false); }}>×</span></button>
      <div className="nav-groups">{navGroups.map((group) => <div className="nav-group" key={group.title}><div className="nav-caption">{group.title}<span>⌄</span></div>{group.items.map(([icon, label, count]) => <button key={label} className={`nav-link ${activeNav === label ? "active" : ""}`} onClick={() => { setActiveNav(label); setMenuOpen(false); }}><span className="nav-icon">{icon}</span>{label}{count && <small>{count}</small>}</button>)}</div>)}</div>
      <div className="sidebar-bottom"><div className="storage-label"><span>Library storage</span><b>68%</b></div><div className="progress-track"><i style={{ width: "68%" }} /></div><small>1.4 GB of 2 GB used</small></div>
    </aside>

    <section className="main-area">
      <header className="topbar"><button className="mobile-menu" onClick={() => setMenuOpen(!menuOpen)}>☰</button><div className="search"><span>⌕</span><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search all books..." /><kbd>⌘ K</kbd></div><div className="top-actions"><button aria-label="Help">ⓘ</button><button className="notification" aria-label="Notifications">♧<i /></button><button aria-label="Statistics">▥</button><button aria-label="Upload">↑</button><span className="top-divider"/><button className="round-action active" aria-label="Theme">◉</button><button aria-label="Settings">⚙</button><span className="top-divider"/><button className="avatar" title="Neon">N</button></div></header>
      <div className="page-content">
        <div className="welcome-line"><span>✦</span><div><h1>Good morning, <b>Neon</b></h1><p>Your next great read is waiting.</p></div><button className="add-book" onClick={() => setSelected({ title: "Add a book", author: "Use the search bar to explore your library", genre: "New book", color: "#4965d6" })}>＋ <span>Add book</span></button></div>
        {activeNav !== "Dashboard" && <div className="view-notice">Viewing <b>{activeNav}</b> · Your library overview is shown below.</div>}
        <div className="insights-grid">
          <section className="insight panel streak"><div className="panel-title"><span className="mini-icon orange">♨</span><h2>Reading streak</h2><button>···</button></div><div className="streak-number">🔥 <b>6</b></div><span className="subtle centered">days streak</span><div className="best-streak">✧ Best: 24 days</div><div className="week-dots">{[1, 1, 1, 1, 1, 1, 0].map((x, i) => <i className={x ? "done" : ""} key={i} />)}</div><span className="subtle centered">Last 7 days</span></section>
          <section className="insight panel currently"><div className="panel-title"><span className="mini-icon blue">▣</span><h2>Currently reading</h2><button>···</button></div>{reading.slice(0, 2).map((book) => <div className="reading-item" key={book.title} onClick={() => setSelected(book)}><BookCover book={book} compact /><div className="reading-info"><b>{book.title}</b><span>{book.author}</span><div className="progress-track"><i style={{ width: `${book.progress}%` }} /></div></div><small>{book.progress}%</small></div>)}</section>
          <section className="insight panel goal-card"><div className="panel-title"><span className="mini-icon violet">◉</span><h2>Reading goal 2026</h2><button>···</button></div><div className="goal-ring" style={{ "--goal-pct": `${Math.min(100, completed.length / goal * 100)}%` }}><div><b>{completed.length}</b><span>of {goal}</span></div></div><div className="goal-footer"><span>{Math.round(completed.length / goal * 100)}% complete</span><button onClick={() => setGoal(goal + 1)} title="Increase goal">↗</button></div></section>
          <section className="insight panel dna-card"><div className="panel-title"><span className="mini-icon purple">✦</span><h2>Reading DNA</h2><button>···</button></div><h3>“The curious explorer”</h3>{[["Length", "Short", 62, "green"], ["Variety", "Eclectic", 78, "orange"], ["Rhythm", "Steady", 58, "yellow"], ["Time", "Evening", 88, "purple"], ["Speed", "Steady pace", 68, "pink"]].map(([label, value, width, color]) => <div className="dna-row" key={label}><span>{label}</span><div className="progress-track"><i className={color} style={{ width: `${width}%` }} /></div><b>{value}</b></div>)}<small>Based on your reading habits</small></section>
          <section className="insight panel challenge"><div className="panel-title"><span className="mini-icon blue">⚒</span><h2>Monthly challenge</h2><button>···</button></div><div className="challenge-art">✦</div><h3>Page turner</h3><p>Read 500 pages this month</p><div className="progress-track"><i style={{ width: "37%" }} /></div><div className="challenge-count"><b>186</b> / 500</div></section>
        </div>
        <Shelf title="Discover something new" icon="✧" items={visibleBooks.slice(0, 8)} onSelect={setSelected} />
        <Shelf title="Recently added" icon="✦" items={[...visibleBooks].reverse().slice(0, 8)} onSelect={setSelected} />
        <section className="bottom-strip"><span className="online-dot"/> All changes synced <span>·</span> Last sync just now <button>Manage library ↗</button></section>
      </div>
    </section>
    {selected && <div className="modal-backdrop" onClick={() => setSelected(null)}><div className="book-modal panel" onClick={(e) => e.stopPropagation()}><button className="modal-close" onClick={() => setSelected(null)}>×</button><BookCover book={selected} /><div><span className="eyebrow">{selected.genre}</span><h2>{selected.title}</h2><p>{selected.author}</p><button className="add-book modal-button" onClick={() => setSelected(null)}>Open book details ↗</button></div></div></div>}
  </main>;
}
