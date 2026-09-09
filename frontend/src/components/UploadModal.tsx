import { FormEvent, useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";

interface UploadModalProps {
	show: boolean;
	onHide: () => void;
	onUpload: (title: string, file: File) => Promise<boolean>;
	isSubmitting: boolean;
}

export function UploadModal({ show, onHide, onUpload, isSubmitting }: UploadModalProps) {
	const [title, setTitle] = useState("");
	const [selectedFile, setSelectedFile] = useState<File | null>(null);
	const [localError, setLocalError] = useState<string | null>(null);

	async function handleSubmit(event: FormEvent<HTMLFormElement>) {
		event.preventDefault();
		setLocalError(null);

		if (!title.trim() || !selectedFile) {
			setLocalError("Укажите название и выберите файл");
			return;
		}

		const success = await onUpload(title.trim(), selectedFile);
		if (success) {
			setTitle("");
			setSelectedFile(null);
			onHide();
		}
	}

	return (
		<Modal show={show} onHide={onHide} centered>
			<Form onSubmit={handleSubmit}>
				<Modal.Header closeButton>
					<Modal.Title>Добавить файл</Modal.Title>
				</Modal.Header>
				<Modal.Body>
					{localError && <div className="alert alert-danger p-2 mb-3">{localError}</div>}
					<Form.Group className="mb-3">
						<Form.Label>Название</Form.Label>
						<Form.Control
							value={title}
							onChange={(event) => setTitle(event.target.value)}
							placeholder="Например, Договор с подрядчиком"
							disabled={isSubmitting}
						/>
					</Form.Group>
					<Form.Group>
						<Form.Label>Файл</Form.Label>
						<Form.Control
							type="file"
							onChange={(event) => {
								const target = event.target as HTMLInputElement;
								setSelectedFile(target.files?.[0] ?? null);
							}}
							disabled={isSubmitting}
						/>
					</Form.Group>
				</Modal.Body>
				<Modal.Footer>
					<Button variant="outline-secondary" onClick={onHide} disabled={isSubmitting}>
						Отмена
					</Button>
					<Button type="submit" variant="primary" disabled={isSubmitting}>
						{isSubmitting ? "Загрузка..." : "Сохранить"}
					</Button>
				</Modal.Footer>
			</Form>
		</Modal>
	);
}
