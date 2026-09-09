import { AlertItem, FileItem } from "../types";

const API_BASE = "http://localhost:8000";

export async function fetchFiles(): Promise<FileItem[]> {
	const response = await fetch(`${API_BASE}/files`, { cache: "no-store" });
	if (!response.ok) throw new Error("Не удалось загрузить файлы");
	return response.json();
}

export async function fetchAlerts(): Promise<AlertItem[]> {
	const response = await fetch(`${API_BASE}/alerts`, { cache: "no-store" });
	if (!response.ok) throw new Error("Не удалось загрузить алерты");
	return response.json();
}

export async function uploadFileAPI(title: string, file: File): Promise<void> {
	const formData = new FormData();
	formData.append("title", title);
	formData.append("file", file);

	const response = await fetch(`${API_BASE}/files`, {
		method: "POST",
		body: formData,
	});

	if (!response.ok) throw new Error("Не удалось загрузить файл");
}
