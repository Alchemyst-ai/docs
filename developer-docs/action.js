const { fetchOpenApiJson, PLATFORM_BASE_URLS } = require("./ctx.js");
const {
	readFileSync,
	writeFileSync,
	mkdirSync,
	readdirSync,
	existsSync,
	lstatSync,
	unlinkSync,
	statSync,
	rmdirSync,
} = require("fs");

const path = require("path");

const openApiJsonPath = path.join(__dirname, "api-reference", "openapi.json");

const apiReferenceEndpointsDir = path.join(
	__dirname,
	"api-reference",
	"endpoint",
);

/**
 * Updates the OpenAPI documentation by fetching the latest OpenAPI JSON from the specified branch
 * and merging it with the current OpenAPI JSON.
 *
 * @param {string} [branch="main"] - The branch from which to fetch the OpenAPI JSON.
 * @returns {Promise<Object>} The updated OpenAPI JSON object.
 */
const updateDocsOpenApi = async (branch = "main") => {
	console.log("Updating OpenAPI docs");

	const currentOpenApiJson = JSON.parse(readFileSync(openApiJsonPath, "utf8"));
	const fetchedOpenApiJson = await fetchOpenApiJson(branch);

	if (!fetchedOpenApiJson) return currentOpenApiJson;

	const openApiJson = { ...currentOpenApiJson, ...fetchedOpenApiJson };

	writeFileSync(openApiJsonPath, JSON.stringify(openApiJson, null, 2));

	return openApiJson;
};

/**
 * Creates an MDX file for the API reference endpoint based on the provided OpenAPI specification and path.
 *
 * @param {Record<string, any>} openApiSpec - The OpenAPI specification object.
 * @param {string} endPointPath - The path of the API endpoint.
 * @returns {Promise<string>}
 */
const createApiReferenceMdxFiles = (openApiSpec, endPointPath) => {
	pathData = openApiSpec["paths"][endPointPath];

	const directoryToWrite = endPointPath
		.split("/")
		.filter((entry) => entry.length > 0);

	mkdirSync(path.join(apiReferenceEndpointsDir, ...directoryToWrite), {
		recursive: true,
	});

	const methods = Object.keys(pathData);

	const filesContent = methods.map((method) => {
		const content = `---
title: '${pathData[method].summary ?? endPointPath}'
openapi: '${method.toUpperCase()} ${endPointPath}'
---`;
		return content;
	});

	methods.forEach((method, idx) => {
		const filePath = path.join(
			apiReferenceEndpointsDir,
			...directoryToWrite,
			`${method.toLowerCase()}.mdx`,
		);
		console.log(`Writing content for ${method} ${endPointPath} to ${filePath}`);
		writeFileSync(filePath, filesContent[idx]);
	});
};

/**
 * Generates MDX files for API reference endpoints by updating the OpenAPI JSON and processing endpoints.
 *
 * @param {string} [branch="main"] - The branch from which to fetch the OpenAPI JSON.
 * @returns {Promise<void>}
 */
const generateMdx = async (branch = "main") => {
	console.log(`Generating MDX files for ${branch} branch`);
	const updatedOpenApiJson = await updateDocsOpenApi(branch);

	Object.keys(updatedOpenApiJson["paths"]).forEach((path) => {
		createApiReferenceMdxFiles(updatedOpenApiJson, path);
	});
};

const walk = (dir, fileList = []) => {
	const files = readdirSync(dir);
	files.forEach((file) => {
		const filePath = path.join(dir, file);
		const stat = statSync(filePath);
		if (stat.isDirectory()) {
			walk(filePath, fileList);
		} else if (file.endsWith(".mdx")) {
			fileList.push(filePath);
		}
	});
	return fileList;
};

const fetchDocsJson = () => {
	const data = readFileSync(path.join(__dirname, "docs.json"), {
		encoding: "utf-8",
	});

	return JSON.parse(data);
};

const generateNewDocsJson = () => {
	const endpointFiles = walk(apiReferenceEndpointsDir)
		.filter((entry) => !!entry && entry.length > 0)
		.map((entry) => entry.slice(entry.indexOf("api-reference"), entry.length-4));
	console.log(endpointFiles);

	let docsJson = fetchDocsJson();

	const apiReferencesTab = docsJson.navigation.tabs
		.filter((entry) => entry.tab === "API reference")
		.pop();

	if (!apiReferencesTab) {
		throw new Error("No API References tab found in docs.json!");
	}
	let endpointExamplesGroup = apiReferencesTab.groups
		.filter((group) => group.group === "Endpoint examples")
		.pop();

	if (!endpointExamplesGroup) {
		throw new Error("No Endpoint Examples group found in API References tab!");
	}

	const newDocsJson = {
		...docsJson,
		navigation: {
			...docsJson.navigation,
			tabs: [
				...docsJson.navigation.tabs.filter(
					(entry) => entry.tab !== "API reference",
				),
				{
					tab: "API reference",
					groups: [
						{
							group: "API documentation",
							pages: ["api-reference/introduction"],
						},
						{
							group: "Endpoint examples",
							pages: endpointFiles,
						},
					],
				},
			],
		},
	};

	writeFileSync("docs.json", JSON.stringify(newDocsJson, null, 2));

	return endpointFiles;
};

const deleteAllAutogenFiles = async () => {
	const deleteFolderRecursive = (folderPath) => {
		if (existsSync(folderPath)) {
			readdirSync(folderPath).forEach((file) => {
				const curPath = path.join(folderPath, file);
				if (lstatSync(curPath).isDirectory()) {
					deleteFolderRecursive(curPath);
				} else {
					unlinkSync(curPath);
				}
			});
			rmdirSync(folderPath);
		}
	};

	deleteFolderRecursive(apiReferenceEndpointsDir);
	mkdirSync(apiReferenceEndpointsDir, { recursive: true });
}

deleteAllAutogenFiles().then(generateMdx).then(setTimeout(generateNewDocsJson, 5000));
