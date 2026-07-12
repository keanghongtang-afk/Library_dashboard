import { Link } from "react-router-dom";
export default function Side(){
    return (
        <div className="sidebar col-md-2 col-lg-3 col-2 border border-5
                        d-flex justify-content-center align-items-center flex-column">
            <Link to={"/fav"} className="text-decoration-none text-dark">Favorite</Link>
            <Link to={"/brow"} className="text-decoration-none text-dark">Borrow</Link>
            <Link to={"/read"} className="text-decoration-none text-dark">Read</Link>
            <Link to={"/history"} className="text-decoration-none text-dark">History</Link>
            <Link to={"/setting"} className="text-decoration-none text-dark">Setting</Link>
            <Link to={"/profile"} className="text-decoration-none text-dark">Profile</Link>
        </div>
    );
}