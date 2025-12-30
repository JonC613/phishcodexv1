import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import axios from 'axios'
import {
  Button,
  Table,
  TableHeader,
  TableRow,
  TableBody,
  TableHeaderCell,
  TableCell,
  Title3,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Input,
  Textarea,
  makeStyles,
  Caption1,
  Badge,
  Spinner
} from '@fluentui/react-components'
import { Comment, CommentCreate, RelistenSongResponse, SetlistSet, ShowDetailResponse } from '../types/api'

const useStyles = makeStyles({
  container: { maxWidth: '900px', margin: '0 auto', padding: '24px' },
  section: { marginTop: '16px' },
  comments: { marginTop: '20px' }
})

export default function ShowDetail() {
  const { showdate } = useParams()
  const [data, setData] = useState<ShowDetailResponse | null>(null)
  const [comments, setComments] = useState<Comment[]>([])
  const [commentBody, setCommentBody] = useState('')
  const [displayName, setDisplayName] = useState('')
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()
  const styles = useStyles()

  useEffect(() => {
    const load = async () => {
      const res = await axios.get<ShowDetailResponse>(`/api/shows/${showdate}`)
      setData(res.data)
      const c = await axios.get<Comment[]>(`/api/shows/${showdate}/comments`)
      setComments(c.data)
      setLoading(false)
    }
    load()
  }, [showdate])

  const openSong = async (title: string, index: number) => {
    const res = await axios.get<RelistenSongResponse>(`/api/shows/${showdate}/relisten/song`, {
      params: { title, index }
    })
    const url = res.data.relisten_url || res.data.fallback_url
    window.open(url, '_blank')
  }

  const submitComment = async () => {
    const payload: CommentCreate = { body: commentBody, display_name: displayName || undefined }
    const res = await axios.post<Comment>(`/api/shows/${showdate}/comments`, payload)
    setComments((prev) => [res.data, ...prev])
    setCommentBody('')
  }

  if (loading || !data) return <Spinner label="Loading" />

  return (
    <div className={styles.container}>
      <Breadcrumb>
        <BreadcrumbItem>
          <BreadcrumbLink onClick={() => navigate('/')}>Home</BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbItem>{showdate}</BreadcrumbItem>
      </Breadcrumb>

      <Title3>{data.show.venue || 'Venue'} - {data.show.city}</Title3>
      <Button appearance="primary" onClick={() => window.open(data.relisten.show_url, '_blank')}>
        Listen to entire show
      </Button>

      <div className={styles.section}>
        {data.setlist.map((set: SetlistSet, setIndex) => (
          <div key={set.name} style={{ marginBottom: 12 }}>
            <Caption1>{set.name}</Caption1>
            <Table aria-label="setlist">
              <TableHeader>
                <TableRow>
                  <TableHeaderCell>Song</TableHeaderCell>
                  <TableHeaderCell>Listen</TableHeaderCell>
                </TableRow>
              </TableHeader>
              <TableBody>
                {set.songs.map((song, idx) => (
                  <TableRow id={`song-${idx}`} key={`${song.title}-${idx}`}>
                    <TableCell>{song.title}</TableCell>
                    <TableCell>
                      <Button size="small" onClick={() => openSong(song.title, idx)}>
                        Listen
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        ))}
      </div>

      <div className={styles.comments}>
        <Title3>Comments</Title3>
        <Input placeholder="Display name (optional)" value={displayName} onChange={(_, d) => setDisplayName(d.value)} />
        <Textarea
          placeholder="Share your thoughts"
          value={commentBody}
          onChange={(_, d) => setCommentBody(d.value)}
        />
        <Button appearance="primary" onClick={submitComment} disabled={!commentBody.trim()}>
          Post comment
        </Button>
        <div style={{ marginTop: 12 }}>
          {comments.map((c) => (
            <div key={c.id} style={{ marginBottom: 10 }}>
              <Badge>{c.display_name || 'Anonymous'}</Badge>
              <Caption1> {new Date(c.created_at).toLocaleString()}</Caption1>
              <div>{c.body}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
