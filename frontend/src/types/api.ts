export type ShowCard = {
  showdate: string;
  venue?: string;
  city?: string;
  state?: string;
  country?: string;
  showid?: number;
};

export type PaginatedShows = {
  items: ShowCard[];
  next_cursor: string | null;
};

export type Song = {
  title: string;
  position: number;
};

export type SetlistSet = {
  name: string;
  songs: Song[];
};

export type ShowDetailResponse = {
  show: ShowCard;
  setlist: SetlistSet[];
  relisten: { show_url: string };
};

export type RelistenSongResponse = {
  mapping_status: string;
  relisten_url?: string | null;
  fallback_url: string;
  track_found: boolean;
  fallback_show: boolean;
};

export type Comment = {
  id: number;
  showdate: string;
  display_name?: string;
  body: string;
  created_at: string;
};

export type CommentCreate = {
  display_name?: string;
  body: string;
};
