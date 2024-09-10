import { createBrowserRouter } from "react-router-dom";
import Background from "./routes/background";
import Root from "./routes/root";

const router = createBrowserRouter([
	{
		path: "/",
		element: <Root />,
		children: [
			{
				path: "/background",
				element: <Background />,
			},
		],
		loader: async ({ request }) => {
			const url = new URL(request.url);
			const data = new URLSearchParams(url.search);

			if (data.get("queryText") == null) {
				return null;
			}

			return fetch(
				"/api/?".concat(
					new URLSearchParams({
						query: data.get("queryText") ?? "",
					}).toString(),
				),
				{
					method: "GET",
				},
			);
		},
	},
]);

export default router;