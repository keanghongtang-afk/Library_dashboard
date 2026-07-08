
export default function Card({ header, content }) {
    return (
        <div className="col-6 col-md-4 col-lg-4 mb-3">
            <div className="border border-2 rounded p-3 h-100">
                <h5>{header}</h5>
                <p>{content}</p>
            </div>
        </div>
    );
}
