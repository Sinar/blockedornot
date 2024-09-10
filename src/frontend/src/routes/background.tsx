import { Link } from "react-router-dom";

export default function Background() {
	return (
		<>
			<h1 className="mb-5">
				<Link className="text-reset text-decoration-none" to="/">
					Bloocked or Not
				</Link>
			</h1>

			<h2 className="mb-4">Project background</h2>

			<h3 className="mb-3">Problem Statement</h3>

			<p className="mb-3">
				The recent DNS redirection crisis in Malaysia highlighted the potential
				for internet censorship to limit access to certain websites or content.
				This can have significant implications for freedom of speech,
				information access, and economic activity. To address this issue, there
				is a need for a transparent and easily accessible tool that can inform
				users about the accessibility of domains within the Malaysian internet
				landscape.
			</p>

			<h3 className="mb-3">Project Objective:</h3>

			<p className="mb-3">
				This project aims to develop a web application that enables users to
				quickly and efficiently check whether a specific domain is blocked or
				accessible within Malaysia. The application will provide real-time
				information on domain status, helping users to navigate the internet
				landscape and make informed decisions about accessing online content.
			</p>

			<h3 className="mb-3">Target Audience</h3>

			<ul className="mb-3">
				<li>
					<strong>General public:</strong> Individuals who want to stay informed
					about internet censorship and ensure they can access the content they
					need.
				</li>
				<li>
					<strong>Journalists and researchers:</strong> Professionals who study
					internet freedom and censorship and require data on domain
					accessibility.
				</li>
				<li>
					<strong>Internet service providers (ISPs):</strong> Organizations that
					want to monitor the status of domains and ensure they are complying
					with relevant regulations.
				</li>
				<li>
					<strong>Government agencies:</strong> Authorities responsible for
					internet governance and censorship who need to track the impact of
					their policies on online access.
				</li>
			</ul>

			<h3 className="mb-3">Expected Benefits</h3>

			<ul className="mb-3">
				<li>
					<strong>Increased transparency:</strong> The application will provide
					a public platform for monitoring domain accessibility, promoting
					transparency and accountability in internet governance.
				</li>
				<li>
					<strong>Empowerment of users:</strong> By providing information on
					domain status, the application will empower users to make informed
					choices about accessing online content and advocating for internet
					freedom.
				</li>
				<li>
					<strong>Support for research:</strong> The application will serve as a
					valuable resource for researchers studying internet censorship and its
					impact on society.
				</li>
				<li>
					<strong>Improved internet governance:</strong> The data collected by
					the application can be used to inform policy decisions and improve
					internet governance practices.
				</li>
			</ul>

			<h2 className="mb-3 mt-4">About us: SinarProject</h2>

			<p className="mb-3">
				<a href="https://sinarproject.org">Sinar Project</a> is a Malaysian
				civic tech initiative that promotes transparency, accountability, and
				citizen participation in government affairs. We leverage open data, open
				technology, and policy analysis to empower Malaysians with the
				information they need to hold their government accountable.
			</p>

			<h3 className="mb-3">Our Focus Areas</h3>

			<ul className="mb-3">
				<li>
					<strong>Open Parliament:</strong> We make information about Malaysian
					representatives and their work readily accessible to the public.
				</li>
				<li>
					<strong>Open Government:</strong> We provide tools and resources to
					help citizens access government data, participate in decision-making
					processes, and hold government institutions accountable.
				</li>
				<li>
					<strong>Transparency:</strong> We use innovative approaches to analyze
					open data and uncover potential issues of corruption or inefficiency
					within the government.
				</li>
			</ul>

			<h3 className="mb-3">Join the Movement:</h3>

			<p className="mb-3">
				Sinar Project is committed to fostering a more open and informed
				Malaysian society. You can contribute to our mission by:
			</p>

			<ul className="mb-3">
				<li>Exploring our website to access valuable resources and tools.</li>
				<li>Participating in our workshops and events.</li>
				<li>Volunteering your skills and expertise.</li>
				<li>Donating to support our ongoing efforts.</li>
			</ul>

			<p className="mb-3">
				Together, we can create a more transparent and accountable government
				that serves the needs of all Malaysians.
			</p>
		</>
	);
}
