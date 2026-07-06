import Card from "../component/card";
function Home(){
    return (
        <div className="home mt-3 position-relative">
            <img src="/public/background.jpg" alt="background" className="img-background"/>
            <div className="welcome-msg d-flex justify-content-center align-items-center flex-column">
                <h1 className="fs-2 text-center">Welcome to NewLife Library</h1>
                <p  className="fs-2 text-center">Here you can find your favorite book just by browse through and search with ease.</p>
            </div>
            <div className="book-container mt-5 d-flex flex-row overflow-scroll justify-content-center align-items-center">
                <Card header="Read Book online for free" content="Millions of books available here"/>
                <Card header="Borrow Book" content="Borrow any book you would like"/>
                <Card header="Reserve Books" content="Reserve books that are currently unavailable and get notified when they're ready"/>
                <Card header="Save Favorites" content="Create your personal reading list and easily find your favorite books"/>
                <Card header="Smart Search" content="Search books by title, author, category, or ISBN in seconds"/>
                <Card header="Manage Your Account" content="Track borrowed books, due dates, and your reading history."/>
            </div>
        </div>
    );
}

export default Home;