import { Badge, FormControl, InputGroup } from "react-bootstrap";
import { HouseLock } from "react-bootstrap-icons";
import {
	Form,
	Link,
	Outlet,
	useLoaderData,
	useLocation,
	useOutlet,
} from "react-router-dom";

function Footer() {
	return (
		<div>
			<p className="text-center fs-6 text-secondary">
				<em>
					<Link className="text-reset" to="/">
						Blocked or Not
					</Link>
				</em>{" "}
				checker is brought to you by{" "}
				<strong>
					<a className="text-reset" href="https://sinarproject.org/">
						SinarProject
					</a>
				</strong>{" "}
				|{" "}
				<Link className="text-reset" to="/background">
					Project background
				</Link>{" "}
				|{" "}
				<a className="text-reset" href="https://github.com/Sinar/blockedornot">
					Github repository
				</a>
			</p>
		</div>
	);
}

function Prompt() {
	const search = new URLSearchParams(useLocation().search);
	const queryText = search.get("queryText");

	return (
		<>
			<h1 className="mb-3">
				<Link className="text-reset text-decoration-none" to="/">
					Blocked or Not
				</Link>{" "}
				<span className="fs-6 fw-normal">by SinarProject</span>
			</h1>
			<Form className="mb-5" action="/" method="GET">
				<InputGroup>
					<InputGroup.Text>
						<HouseLock size="32" />
					</InputGroup.Text>
					<FormControl
						size="lg"
						name="queryText"
						defaultValue={queryText ?? ""}
						placeholder="Type URL and press ENTER, e.g. sinarproject.org"
					/>
				</InputGroup>
			</Form>
			<Result />
		</>
	);
}

function Result() {
	const result = useLoaderData();

	if (result === null) {
		return <></>;
	}

	return (
		<div className="mb-3">
			<h2>
				Query result for <em>{result.query}</em>
			</h2>
			<p>
				The specified website is <ResultBadge result={result} />.
			</p>
			<ResultExplanation result={result} />
			{result.measurement && (
				<p>
					For more information please visit the{" "}
					<a href={result.measurement}>measurement report</a> at OONI
				</p>
			)}
		</div>
	);
}

function ResultBadge({ result }) {
	let badge = <Badge bg="success">SAFE</Badge>;

	if (result.blocked) {
		badge = <Badge bg="danger">BLOCKED</Badge>;
	} else if (result.blocked === false && result.different_ip) {
		badge = <Badge bg="warning">LIKELY SAFE</Badge>;
	}

	return badge;
}

function ResultExplanation({ result }) {
	let text = <></>;

	if (result.blocked) {
		text = (
			<p>
				Instead of the intended IP address, this URL is being directed by TMNet
				(AS4788) DNS server to the IP address 175.139.142.25 for websites
				blocked by MCMC.
			</p>
		);
	} else if (result.blocked === false && result.different_ip) {
		text = (
			<p>
				Different sets of IPs were received from our TMNet (AS4788) and a
				well-known public DNS provider. It could be due to the use of Content
				Delivery Network by the website operator.
			</p>
		);
	}

	return text;
}

export default function Root() {
	return (
		<>
			<div className="d-flex flex-column justify-content-between min-vh-100">
				<div className="container pt-5 pb-5">
					{useOutlet() === null ? <Prompt /> : <Outlet />}
				</div>
				<Footer />
			</div>
		</>
	);
}
