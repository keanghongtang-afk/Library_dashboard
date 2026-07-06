
export default function Card({header, content}){
    return (
        <div className="card card-3 p-2 m-3">
            <h5>{header}</h5>
            <p>{content}</p>
        </div>
    );
}