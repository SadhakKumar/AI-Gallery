import { useState, useEffect, useRef } from "react";
import "./App.css";
import axios from "axios";
import { Upload, Search, X, Loader2 } from "lucide-react";

function App() {
  const [gallery, setGallery] = useState([]);
  const [searchedImages, setSearchedImages] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [isUploading, setIsUploading] = useState(false);
  const [searchLimit, setSearchLimit] = useState(3);
  const [isLoadingGallery, setIsLoadingGallery] = useState(true);
  const [isLoadingSearch, setIsLoadingSearch] = useState(false);
  const fileInputRef = useRef(null);

  const imagesPerPage = 12;

  useEffect(() => {
    fetchGallery();
  }, []);

  async function fetchGallery() {
    try {
      setIsLoadingGallery(true);
      const response = await axios.get(
        `${import.meta.env.VITE_BACKEND_SERVER_URL}/all-images`,
        {
          headers: {
            "ngrok-skip-browser-warning": "true",
          },
        }
      );
      console.log("response:", response.data);
      setGallery(response.data);
    } catch (error) {
      console.error("Error fetching gallery:", error);
    } finally {
      setIsLoadingGallery(false);
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setIsSearching(false);
      setCurrentPage(1);
      return;
    }

    try {
      setIsSearching(true);
      setIsLoadingSearch(true);
      const response = await axios.get(
        `${
          import.meta.env.VITE_BACKEND_SERVER_URL
        }/similar-images?caption=${searchQuery}&top_k=${searchLimit}`,
        {
          headers: {
            "ngrok-skip-browser-warning": "true",
          },
        }
      );
      console.log(response.data);
      setSearchedImages(response.data);
      setCurrentPage(1);
    } catch (error) {
      console.error("Error fetching searched images:", error);
    } finally {
      setIsLoadingSearch(false);
    }
  };

  const clearSearch = () => {
    setSearchQuery("");
    setIsSearching(false);
    setSearchedImages([]);
    setCurrentPage(1);
    setIsLoadingSearch(false);
  };

  const handleFileUpload = async (e) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setIsUploading(true);
    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    try {
      await axios.post(
        `${import.meta.env.VITE_BACKEND_SERVER_URL}/gallery/upload`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "ngrok-skip-browser-warning": "true",
          },
        }
      );
      await fetchGallery();
    } catch (error) {
      console.error("Error uploading files:", error);
    } finally {
      setIsUploading(false);
    }
  };

  // Determine which images to display
  const displayImages = isSearching
    ? searchedImages.relative_path || []
    : gallery.images || [];

  const totalImages = displayImages.length;

  // Pagination logic
  const indexOfLastImage = currentPage * imagesPerPage;
  const indexOfFirstImage = indexOfLastImage - imagesPerPage;
  const currentImages = displayImages.slice(
    indexOfFirstImage,
    indexOfLastImage
  );
  const totalPages = Math.ceil(totalImages / imagesPerPage);

  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <h1 className="title">AI Gallery</h1>
          <p className="subtitle">Intelligent Image Search & Management</p>
        </div>
      </header>

      {/* Search & Upload Bar */}
      <div className="controls-wrapper">
        <div className="controls-container">
          <form onSubmit={handleSearch} className="search-form">
            <div className="search-input-wrapper">
              <Search className="search-icon" size={20} />
              <input
                type="text"
                placeholder="Search images by description..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input"
                disabled={isLoadingSearch}
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={clearSearch}
                  className="clear-button"
                  aria-label="Clear search"
                  disabled={isLoadingSearch}
                >
                  <X size={18} />
                </button>
              )}
            </div>

            <div className="limit-input-wrapper">
              <input
                type="number"
                min="1"
                max="100"
                value={searchLimit}
                onChange={(e) =>
                  setSearchLimit(Math.max(1, parseInt(e.target.value)))
                }
                className="limit-input"
                aria-label="Number of results"
                disabled={isLoadingSearch}
              />
              <span className="limit-label">results</span>
            </div>

            <button
              type="submit"
              className="search-button"
              disabled={isLoadingSearch}
            >
              {isLoadingSearch ? (
                <>
                  <Loader2 className="spinner" size={18} />
                  <span>Searching...</span>
                </>
              ) : (
                "Search"
              )}
            </button>
          </form>

          <button
            onClick={() => fileInputRef.current?.click()}
            className="upload-button"
            disabled={isUploading}
          >
            {isUploading ? (
              <>
                <Loader2 className="spinner" size={20} />
                <span>Uploading...</span>
              </>
            ) : (
              <>
                <Upload size={20} />
                <span>Upload</span>
              </>
            )}
          </button>
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept="image/*"
            onChange={handleFileUpload}
            style={{ display: "none" }}
          />
        </div>
      </div>

      {/* Search Status */}
      {isSearching && !isLoadingSearch && (
        <div className="search-status">
          <p>
            Found {totalImages} result{totalImages !== 1 ? "s" : ""} for "
            {searchQuery}"
          </p>
          <button onClick={clearSearch} className="view-all-link">
            View all images
          </button>
        </div>
      )}

      {/* Gallery Grid */}
      <main className="gallery-container">
        {isLoadingGallery && !isSearching ? (
          <div className="empty-state">
            <div className="empty-content">
              <Loader2 className="spinner-large" size={48} />
              <h2>Loading gallery...</h2>
              <p>Please wait while we fetch your images</p>
            </div>
          </div>
        ) : isLoadingSearch ? (
          <div className="empty-state">
            <div className="empty-content">
              <Loader2 className="spinner-large" size={48} />
              <h2>Searching...</h2>
              <p>Finding images that match "{searchQuery}"</p>
            </div>
          </div>
        ) : totalImages === 0 ? (
          <div className="empty-state">
            <div className="empty-content">
              <h2>{isSearching ? "No results found" : "No images yet"}</h2>
              <p>
                {isSearching
                  ? "Try adjusting your search terms"
                  : "Upload some images to get started"}
              </p>
            </div>
          </div>
        ) : (
          <>
            <div className="gallery-grid">
              {searchedImages && isSearching
                ? searchedImages.relative_path.map((image, index) => (
                    <div
                      key={`${index}`}
                      className="gallery-item"
                      style={{ animationDelay: `${index * 0.05}s` }}
                    >
                      <img
                        src={`${image.image_path}`}
                        alt={"Gallery Image"}
                        className="gallery-image"
                        loading="lazy"
                      />
                      <div className="image-overlay">
                        <p className="image-filename">{image.caption}</p>
                      </div>
                    </div>
                  ))
                : currentImages.map((image, index) => (
                    <div
                      key={`${image.filename}-${index}`}
                      className="gallery-item"
                      style={{ animationDelay: `${index * 0.05}s` }}
                    >
                      <img
                        src={`${image.relative_path}`}
                        alt={image.filename}
                        className="gallery-image"
                        loading="lazy"
                      />
                      <div className="image-overlay">
                        <p className="image-filename">
                          {image.filename || "Gallery Image"}
                        </p>
                      </div>
                    </div>
                  ))}
            </div>

            {/* Pagination & Stats */}
            <div className="footer-controls">
              {totalPages > 1 && !isSearching && (
                <div className="pagination">
                  <button
                    onClick={() => paginate(currentPage - 1)}
                    disabled={currentPage === 1}
                    className="pagination-button"
                  >
                    Previous
                  </button>

                  <div className="pagination-numbers">
                    {[...Array(totalPages)].map((_, index) => {
                      const pageNum = index + 1;
                      // Show first, last, current, and adjacent pages
                      if (
                        pageNum === 1 ||
                        pageNum === totalPages ||
                        (pageNum >= currentPage - 1 &&
                          pageNum <= currentPage + 1)
                      ) {
                        return (
                          <button
                            key={pageNum}
                            onClick={() => paginate(pageNum)}
                            className={`pagination-number ${
                              currentPage === pageNum ? "active" : ""
                            }`}
                          >
                            {pageNum}
                          </button>
                        );
                      } else if (
                        pageNum === currentPage - 2 ||
                        pageNum === currentPage + 2
                      ) {
                        return (
                          <span key={pageNum} className="pagination-ellipsis">
                            ...
                          </span>
                        );
                      }
                      return null;
                    })}
                  </div>

                  <button
                    onClick={() => paginate(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className="pagination-button"
                  >
                    Next
                  </button>
                </div>
              )}

              <div className="image-count">
                Showing {indexOfFirstImage + 1}–
                {Math.min(indexOfLastImage, totalImages)} of {totalImages}{" "}
                images
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
