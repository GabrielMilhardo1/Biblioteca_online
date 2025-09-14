export interface Book {
  id: number;
  title: string;
  author: string;
  isbn: string;
  publication_date: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface BookFormData {
  title: string;
  author: string;
  isbn: string;
  publication_date: string;
  description?: string;
}

export type BookUpdateData = Partial<BookFormData>;