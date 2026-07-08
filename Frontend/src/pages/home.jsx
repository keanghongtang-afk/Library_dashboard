import Card from "../component/card";
function Home() {

  const cards = [
    {
      header: "Read Book online for free",
      content: "Millions of books available here",
    },
    {
      header: "Borrow Book",
      content: "Borrow any book you would like",
    },
    {
      header: "Reserve Books",
      content: "Reserve books that are currently unavailable and get notified when they're ready",
    },
    {
      header: "Save Favorites",
      content: "Create your personal reading list and easily find your favorite books",
    },
    {
      header: "Smart Search",
      content: "Search books by title, author, category, or ISBN in seconds",
    },
    {
      header: "Manage Your Account",
      content: "Track borrowed books, due dates, and your reading history.",
    },
  ];

  return (
    <div className="home mt-3 position-relative">
      <img src="/background.jpg" alt="background" className="img-background" />
      <div className="welcome-msg d-flex justify-content-center align-items-center flex-column">
        <h1 className="fs-2 text-center">Welcome to NewLife Library</h1>
        <p className="fs-2 text-center">Here you can find your favorite book just by browse through and search with ease.</p>
      </div>
      <div className="row mt-5 g-3 justify-content-center">
        {cards.map((card, index) => (
          <Card
            key={index}
            header={card.header}
            content={card.content}
          />
        ))}
      </div>
      <h3>Browse Book here!</h3>
      <div className="row g-4 books-brief justify-content-center">
        {cards.map((card, index) => (
          <div className="col-sm-12 col-md-6 col-lg-4 d-flex justify-content-center">
            <div className="book-3d">
              <div className="book-3d-inner">
                <img src="/book-cover/cover.jpg" alt="cover" className="book-3d-cover" />
                <div className="book-3d-spine"></div>
                <div className="book-3d-pages"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;