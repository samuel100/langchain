import os
import tempfile
from typing import List, Optional

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders.unstructured import UnstructuredFileIOLoader


class AzureAIDataLoader(BaseLoader):
    """Load from Azure AI Data."""

    def __init__(self, url: str, glob: Optional[str] = None):
        """Initialize with URL to a data asset or storage location
        ."""
        self.url = url
        """URL to the data asset or storage location."""
        self.glob_pattern = glob
        """Optional glob pattern to select files. Defaults to None."""

    def load(self) -> List[Document]:
        """Load documents."""
        try:
            from azureml.fsspec import AzureMachineLearningFileSystem
        except ImportError as exc:
            raise ImportError(
                "Could not import azureml-fspec package."
                "Please install it with `pip install azureml-fsspec`."
            ) from exc

        fs = AzureMachineLearningFileSystem(self.url)

        remote_paths_list = []
        if self.glob_pattern:
            remote_paths_list = fs.glob(self.glob_pattern)
        else:
            remote_paths_list = fs.ls()

        docs = []
        for remote_path in remote_paths_list:
            with fs.open(remote_path) as f:
                loader = UnstructuredFileIOLoader(file=f)
                docs.extend(loader.load())

        return docs
