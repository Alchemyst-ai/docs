import dotenv from "dotenv";
import AlchemystAI from "@alchemystai/sdk";

dotenv.config();

const client = new AlchemystAI({
  apiKey: process.env.ALCHEMYST_AI_API_KEY,
});

async function main() {
  let time = performance.now();

  // await client.v1.context.add({
  //   documents: [
  //     {
  //       content: "The content of the document",
  //     },
  //   ],
  //   context_type: "resource",
  //   source: "web-upload",
  //   scope: "internal",
  //   metadata: {
  //     fileName: "notes.txt",
  //     fileType: "text/plain",
  //     lastModified: new Date().toISOString(),
  //     fileSize: 1024,
  //     groupName: ["group1", "group2"],
  //   },
  // });

  // console.log("Time taken to add context:", performance.now() - time, "ms");

  time = performance.now();
  const { contexts } = await client.v1.context.search(
    {
      query: "Your search query here",
      similarity_threshold: 0.8,
      minimum_similarity_threshold: 0.5,
      scope: "internal",
      body_metadata: {
        // Optional - can be null
        size: 100,
        fileType: "ai/conversation",
        fileName: "chatgpt-convo-1",
        groupName: ["project-name"],
      },
    },
    {
      query: {
        mode: "fast",
        // metadata: "false",
      },
    },
  );

  console.log("Time taken to search context:", performance.now() - time, "ms");
}

main();
