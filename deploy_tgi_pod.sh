

#/bin/bash

# deploy fbellame/mistral-7b-json-quizz-fine-tuned model on a NVIDIA GeForce RTX 3080 10 Go VRAM runpod, cost about 0.18$/hour

export RUNPOD_KEY=""

curl --request POST \
  --header 'content-type: application/json' \
  --url "https://api.runpod.io/graphql?api_key=${RUNPOD_KEY}" \
  --data '{"query": "mutation { podFindAndDeployOnDemand( input: { cloudType: ALL, gpuCount: 1, volumeInGb: 50, containerDiskInGb: 40, gpuTypeId: \"NVIDIA GeForce RTX 3080\", name: \"confoo-inference\", imageName: \"ghcr.io/huggingface/text-generation-inference:latest\", dockerArgs: \"--model-id fbellame/mistral-7b-json-quizz-fine-tuned --num-shard 1 --quantize bitsandbytes-nf4\", ports: \"80/http\", volumeMountPath: \"/data\" } ) { id imageName env machineId machine { podHostId } } }"}'
