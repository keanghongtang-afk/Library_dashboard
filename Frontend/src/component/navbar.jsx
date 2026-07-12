import { Link } from "react-router-dom";
function Navbar({islogin}){
    return (islogin?
        <div className="nav 
        border border-2 border-success
        d-flex justify-content-between align-items-center
        p-3">
            <Link to="/" className="text-decoration-none text-dark"><h3>NewLife Library</h3></Link>
            <Link to="/profile" className="text-decoration-none text-dark" ><img src="/profile/profile.jpg" alt="profile-img" className="rounded-circle" width={"50px"} height={"50px"}/></Link>
        </div>
        :
        <div className="nav 
        border border-2 border-success
        d-flex justify-content-between
        p-3">
            <Link to="/" className="text-decoration-none text-dark"><h3>NewLife Library</h3></Link>
            <nav className="d-flex justify-content-between fs-3 g-4">
                <Link to="/auth-page" className="text-decoration-none text-dark">Log In</Link>
                /
                <Link to="/auth-page" className="text-decoration-none text-dark">Sign Up</Link>
            </nav>
        </div>
    );
}

export default Navbar;